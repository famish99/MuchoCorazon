"""
Module for game models
"""
from django.db import models
import caching.base


class DeckUser(caching.base.CachingMixin, models.Model):
    """
    Class to get around the limitation that Deck can't be ForeignKey'd
    to either Session or Player
    """

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(DeckUser, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Player """
        app_label = "game"
        verbose_name = "Deck User"


class Session(DeckUser):
    """
    Django model to store game state
    """

    turn = models.PositiveSmallIntegerField()
    phase = models.PositiveSmallIntegerField()

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Player """
        app_label = "game"
        verbose_name = "Game session"
