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
    """

    user = models.ForeignKey(DeckUser, related_name="decks")
    _card_list = PickledObjectField()
    name = models.CharField(max_length=16)
    show_prop = models.CharField(
            max_length=16, choices=SHOW_CHOICES, null=True)

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Deck, self).__init__(*args, **kwargs)
        self._card_list = []
    
    def __unicode__(self):
        join_str = ', '
        repr_str = "%s: %s" % (self.name, join_str.join(
                [ card.name for card in self.card_list ])
                )
        return repr_str

    def add_card(self, input_card, **kwargs):
        """
        Add card to the deck

        @param top: True: insert to top of the deck,
            False: insert to bottom of deck
        """
        self.cards.add(input_card)
        top = kwargs.get("top", True)
        if top:
            self._card_list.append(input_card.id)
        else:
            self._card_list.insert(0, input_card.id)
        if kwargs.get("save"):
            self.save()

    def remove_card(self, input_card, **kwargs):
        """
        Remove specific card from the deck
        """
        pass

    def pop_card(self, **kwargs):
        """
        Remove card from the (top | bottom) of the deck

        @param top: True: remove from top of the deck,
            False: remove from bottom of deck
        @return: A card from the (top | bottom) of the deck
        """
        top = kwargs.get("top", True)
        if kwargs.get("index"):
            index = kwargs.get("index")
        elif not top:
            index = 0
        else:
            index = -1
        card_id = self._card_list.pop(index)
        card = self.cards.get(id=card_id)
        self.cards.remove(card)
        if kwargs.get("save"):
            self.save()
        return card

    def shuffle(self, **kwargs):
        """
        Shuffle deck order
        """
        random.shuffle(self._card_list)
        self.save()

    @property
    def card_list(self, **kwargs):
        """
        Present a full list of cards in order

        @return: A list of card objects in deck order
        """
        return [ self.cards.get(id=card_id) for card_id in self._card_list ]

    class Meta:
        """ Metadata class for Deck """
        app_label = "game"
        verbose_name = "Deck"
