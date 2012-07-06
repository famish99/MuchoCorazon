"""
Module for game models
"""
from game.models.player import Player
from game.models.deck import Deck
from django.db import models
import caching.base


class Session(caching.base.CachingMixin, models.Model):
    """
    Django model to store game state
    """

    players = models.ForeignKey(Player)
    stacks = models.ForeignKey(Deck)
    turn = models.PositiveSmallIntegerField()
    phase = models.PositiveSmallIntegerField()

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Player """
        app_label = "game"
        verbose_name = "Game session"
