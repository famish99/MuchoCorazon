"""
Deck module
"""
from game.models.session import DeckUser
from django.db import models
from picklefield.fields import PickledObjectField
import caching.base

SHOW_CHOICES = (
        ("show_none", "Show None"),
        ("show_top", "Show Top"),
        ("show_all", "Show All"),
        )

class Deck(caching.base.CachingMixin, models.Model):
    """
    Deck class
    """

    user = models.ForeignKey(DeckUser, related_name="decks")
    card_list = PickledObjectField()
    name = models.CharField(max_length=16)
    show_prop = models.CharField(max_length=16, choices=SHOW_CHOICES)

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Deck, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Deck """
        app_label = "game"
        verbose_name = "Deck"
