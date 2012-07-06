"""
Module for user models
"""
from cuore.models.player import Player
from django.db import models
import caching.base


class User(caching.base.CachingMixin, models.Model):
    """
    Django model to store user info
    """

    name = models.CharField(max_length=16)
    players = models.ForeignKey(Player)

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Player """
        app_label = "cuore"
        verbose_name = "User info"
