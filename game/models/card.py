"""
Module containing the card model
"""
from game.models.deck import Deck
from django.db import models
import caching.base


class Card(caching.base.CachingMixin, models.Model):
    """
    Django model to store a single card
    """

    deck = models.ForeignKey(Deck, related_name="cards", null=True)
    name = models.CharField(max_length=32)
    image = models.ImageField(upload_to="card_images")

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Card """
        app_label = "game"
        verbose_name = "Card"
