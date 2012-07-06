"""
Module for player models
"""
from cuore.models.deck import Deck
from django.db import models
import caching.base


class Player(caching.base.CachingMixin, models.Model):
    """
    Django model to store player info
    """

    decks = models.ForeignKey(Deck, related_name='+')

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Player """
        app_label = "cuore"
        verbose_name = "Player"
