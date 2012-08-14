"""
Deck module
"""
from game.models.session import DeckUser
from game.models.card import CardUser
from django.db import models
from picklefield.fields import PickledObjectField
import random
import caching.base


SHOW_CHOICES = (
        ("none", "Show None"),
        ("top", "Show Top"),
        ("all", "Show All"),
        )


class Deck(CardUser):
    """
    Deck class
    
    Index 0 represents the top of the deck
    """

    user = models.ForeignKey(DeckUser, related_name="decks")
    name = models.CharField(max_length=16)
    _card_list = PickledObjectField()
    show_prop = models.CharField(
            max_length=16, choices=SHOW_CHOICES, null=True)

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Deck, self).__init__(*args, **kwargs)
        if not self._card_list:
            self._card_list = []
    
    def __unicode__(self):
        join_str = ', '
        repr_str = "%s: %s" % (self.name, join_str.join(
                [ card.name for card in self.card_list ])
                )
        return repr_str

    def insert_card(self, input_card, **kwargs):
        """
        Add card to the deck

        @param top: True: insert to top of the deck,
            False: insert to bottom of deck (default True)
        @param index: Remove card at index location, overrides top parameter
        """
        self.cards.add(input_card)
        top = kwargs.get("top", True)
        if kwargs.get("index"):
            index = kwargs.get("index")
        elif not top:
            index = len(self._card_list)
        else:
            index = 0
        self._card_list.insert(index, input_card.id)
        if kwargs.get("save"):
            self.save()

    def insert_cards(self, input_cards, **kwargs):
        """
        Add card to the deck

        @param top: True: insert to top of the deck,
            False: insert to bottom of deck (default True)
        @param queue: For whatever reason you want order preserved on add
        @param index: Insert cards at index location, overrides top parameter
        """
        if kwargs.get("queue", False):
            input_cards.reverse 
        for card in input_cards:
            self.insert_card(card, **kwargs)

    def get_card(self, *args, **kwargs):
        """
        Pick out card at index.
        This can also be accomplished by doing card_list[index], but for
        larger lists, this method would be more efficient.

        @param index: integer location of the card (first argument)
        @param end: integer location of last card to slice (optional)
        @param step: integer stepping of cards to slice (optional)
        @return: The Card object at the location
        """
        index = args[0]
        if len(args) == 2:
            end = args[1]
            return [ self.cards.get(id=index)
                    for index in self._card_list[index:end]
                    ]
        elif len(args) == 3:
            end = args[1]
            step = args[2]
            return [ self.cards.get(id=index)
                    for index in self._card_list[index:end:step]
                    ]
        else:
            return self.cards.get(id=self._card_list[index])

    def search_card(self, input_card, **kwargs):
        """
        Search for specific card from the deck
        """
        return NotImplementedError(
                "Not entirely sure if this will ever be implemented")

    def remove_card(self, **kwargs):
        """
        Remove card from the deck

        @param top: True: remove from top of the deck,
            False: remove from bottom of deck (default True)
        @param index: Remove card at index location, overrides top parameter
        @return: A card from the deck
        """
        top = kwargs.get("top", True)
        if kwargs.get("index"):
            index = kwargs.get("index")
        elif not top:
            index = -1
        else:
            index = 0
        card_id = self._card_list.pop(index)
        card = self.cards.get(id=card_id)
        self.cards.remove(card)
        if kwargs.get("save"):
            self.save()
        return card

    def remove_cards(self, num_cards, **kwargs):
        """
        @param num_cards: number of cards to remove from the deck
        @param index: Remove card at index location
        @return: A card from the deck
        """
        return [ self.remove_card(**kwargs) for cnt in range(num_cards) ]

    def shuffle(self, **kwargs):
        """
        Shuffle deck order
        """
        random.shuffle(self._card_list)
        self.save()

    @property
    def card_list(self):
        """
        Present a full list of cards in order

        @return: A list of card objects in deck order
        """
        return [ self.cards.get(id=card_id) for card_id in self._card_list ]

    @property
    def length(self):
        """
        Return the number of cards in the deck

        @return: An integer representing the number of cards
        """
        return len(self._card_list)

    class Meta:
        """ Metadata class for Deck """
        app_label = "game"
        verbose_name = "Deck"
