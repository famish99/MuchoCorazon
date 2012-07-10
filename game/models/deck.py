"""
Deck module
"""
from game.models.session import DeckUser
from django.db import models
from picklefield.fields import PickledObjectField
import caching.base

SHOW_CHOICES = (
        ("none", "Show None"),
        ("top", "Show Top"),
        ("all", "Show All"),
        )

class Deck(caching.base.CachingMixin, models.Model):
    """
    Deck class
    """

    user = models.ForeignKey(DeckUser, related_name="decks")
    card_list = PickledObjectField()
    name = models.CharField(max_length=16)
    show_prop = models.CharField(
            max_length=16, choices=SHOW_CHOICES, null=True)

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Deck, self).__init__(*args, **kwargs)
        self.card_list = []

    def add_card(self, input_card, **kwargs):
        """
        Add card to the deck

        @param top: True: insert to top of the deck,
            False: insert to bottom of deck
        """
        self.cards.add(input_card)
        top = kwargs.get("top", True)
        if top:
            self.card_list.append(input_card.id)
        else:
            self.card_list.insert(0, input_card.id)

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
        """
        top = kwargs.get("top", True)
        if top:
            card_id = self.card_list.pop()
        else:
            card_id = self.card_list.pop(0)
        card = self.cards.get(id=card_id)
        self.cards.remove(card)
        return card

    def shuffle_deck(self, **kwargs):
        """
        Shuffle deck order
        """
        pass

    class Meta:
        """ Metadata class for Deck """
        app_label = "game"
        verbose_name = "Deck"
