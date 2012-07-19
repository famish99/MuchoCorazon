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

    class Meta:
        """ Metadata class for DeckUser """
        app_label = "game"
        verbose_name = "Deck User"


class Session(DeckUser):
    """
    Django model to store game state
    """

    turn = models.PositiveSmallIntegerField(null=True)
    phase = models.PositiveSmallIntegerField(null=True)
    _player_list = PickledObjectField()

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        if not self._player_list:
            self._player_list = []

    def add_player(self, input_user, **kwargs):
        """
        Add a new player to the game session

        @param user: UserProfile of the user who wants to be added to
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
        import game.models.player as player
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
