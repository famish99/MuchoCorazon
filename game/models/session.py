"""
Module for game models
"""
from django.db import models
from picklefield.fields import PickledObjectField
import caching.base
import random


class DeckUser(caching.base.CachingMixin, models.Model):
    """
    Class to get around the limitation that Deck can't be ForeignKey'd
    to either Session or Player
    """

    classname = models.CharField(max_length=64, editable=False, null=True)

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(DeckUser, self).__init__(*args, **kwargs)

    def add_deck(self, name):
        """
        Add new deck to DeckUser

        @param name: name of deck to be added
        @return: deck that was created
        """
        import game.models.deck as deck

        deck = deck.Deck.objects.create(user=self, name=name)
        return deck

    def save(self, *args, **kwargs):
        """
        Overwrite the save function to save the class name for referencing
        purposes.
        """
        if not self.classname:
            cur_class = self.__class__
            class_str = cur_class.__name__
            while cur_class.__name__ != "DeckUser":
                cur_class = cur_class.__base__().__class__
                class_str = "%s.%s" % (cur_class.__name__, class_str)
            self.classname = class_str
        super(DeckUser, self). save(*args, **kwargs)

    def get_class(self):
        """
        Allow a user to query the main DeckUser table and be able to find
        the associate subclass
        """
        if self.classname == self.__class__.__name__:
            return self
        ptr = self
        for sub_class in self.classname.lower().split('.')[1:]:
            ptr = ptr.__getattribute__(sub_class)
        return ptr
    
    @classmethod
    def draw_cards(cls, from_deck, to_deck, **kwargs):
        """
        Streamline common operation of drawing cards
        """
        if kwargs.get("all"):
            num_cards = from_deck.length
        else:
            num_cards = kwargs.get("num_cards", 1)
        for num in range(num_cards):
            card = from_deck.remove_card()
            to_deck.insert_card(card)

    @property
    def deck_list(self):
        """
        Present a full list of decks

        @return: A dict of deck objects keyed by deck name
        """
        return { deck.name : deck for deck in self.decks.all() }

    class Meta:
        """ Metadata class for DeckUser """
        app_label = "game"
        verbose_name = "Deck User"


class Session(DeckUser):
    """
    Django model to store game state
    """

    turn = models.PositiveSmallIntegerField(default=0)
    phase = models.PositiveSmallIntegerField(default=0)
    _player_list = PickledObjectField()
    phase_list = PickledObjectField()

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        if not self._player_list:
            self._player_list = []
        if not self.phase_list:
            self.phase_list = []

    def next_turn(self, **kwargs):
        """
        Advance the gameplay to the next turn

        @param save: Save model after advancing turn (default: True)
        """
        self.turn = self.turn + 1
        if kwargs.get("save", True):
            self.save()

    def next_phase(self, **kwargs):
        """
        Advance the gameplay to the next phase

        @param save: Save model after advancing phase (default: True)
        """
        self.phase = self.phase + 1
        if self.phase >= len(self.phase_list):
            self.phase = 0
            self.next_turn(save=False)
        if kwargs.get("save", True):
            self.save()

    def current_phase(self):
        """
        Return the current phase
        """
        return self.phase_list[self.phase]

    def current_player(self):
        """
        Return the current player
        """
        player_id = self._player_list[self.turn % len(self._player_list)]
        return self.players.get(id=player_id)

    def add_phase(self, phase_name, **kwargs):
        """
        Add a phase to the phase list

        @param phase_name: Name of the phase to add
        @param save: Save model after adding new player (default: True)
        """
        self.phase_list.append(phase_name)
        if kwargs.get("save", True):
            self.save()

    def add_player(self, input_user, **kwargs):
        """
        Add a new player to the game session

        @param input_user: UserProfile of the user who wants to be added to
            game session
        @param index: Index (seat number) for the player to be added
        @param save: Save model after adding new player (default: True)
        @return: Player object linked to UserProfile and Session.
        """
        import game.models.player as player
        new_player = player.Player.objects.create(
                user=input_user, session=self
                )
        if "index" in kwargs:
            index = kwargs.get("index")
            if self._player_list[index]:
                raise ValueError(
                        "Cannot add player, player already exists at seat %d" %
                        index)
        else:
            index = len(self._player_list)
        self._player_list.insert(index, new_player.id)
        if kwargs.get("save", True):
            self.save()
        return new_player

    def remove_player(self, **kwargs):
        """
        Remove a new player from the game session

        @param index: Index (seat number) for the player to be removed
        @param save: Save model after removing new player (default: True)
        @return: Player object removed
        """
        if "index" in kwargs:
            index = kwargs.get("index")
            if not self._player_list[index]:
                raise ValueError(
                        "Cannot remove player, player does not exists at seat %d" %
                        index)
        else:
            index = -1
        rem_player = self.players.get(id=self._player_list[index])
        self._player_list[index] = None
        if kwargs.get("save", True):
            self.save()
        return rem_player

    def shuffle_players(self, **kwargs):
        """
        Shuffle player order
        """
        random.shuffle(self._player_list)
        self.save()

    def swap_players(self, player_a, player_b, **kwargs):
        """
        Swap two players around

        @param player_a: index of player to swap
        @param player_b: index of player to swap
        """
        self._player_list[player_a], self._player_list[player_b] = (
                self._player_list[player_b], self._player_list[player_a])
        self.save()

    @property
    def player_list(self):
        """
        Present a full list of players in order

        @return: A list of Player objects in order
        """
        p_list = []
        for item in self._player_list:
            if item:
                p_list.append(self.players.get(id=item))
            else:
                p_list.append(None)
        return p_list

    class Meta:
        """ Metadata class for Player """
        app_label = "game"
        verbose_name = "Game session"
