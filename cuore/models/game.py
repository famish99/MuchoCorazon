"""
Module for game models
"""
from cuore.models.player import Player
from django.db import models
import caching.base


class Game(caching.base.CachingMixin, models.Model):
    """
    Django model to store game state
    """

    players = models.ManyToManyField(Player)
    stacks = models.ManyToManyField(Deck)

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Player """
        app_label = "cuore"
        verbose_name = "Game session"
