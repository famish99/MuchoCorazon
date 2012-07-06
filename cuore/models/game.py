"""
Module for game models
"""
from cuore.models.player import Player
from cuore.models.deck import Deck
from django.db import models
import caching.base


class Game(caching.base.CachingMixin, models.Model):
    """
    Django model to store game state
    """

    players = models.ForeignKey(Player)
    stacks = models.ForeignKey(Deck, related_name='+')
    turn = models.PositiveSmallIntegerField()
    phase = models.PositiveSmallIntegerField()

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Player """
        app_label = "cuore"
        verbose_name = "Game session"
