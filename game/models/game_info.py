"""
Module containing the game info model
"""
from django.db import models
from picklefield.fields import PickledObjectField
import caching.base


class GameInfo(caching.base.CachingMixin, models.Model):
    """
    Class containing metadata about games installed
    """

    name = models.CharField(max_length=128, unique=True)
    ref = models.CharField(max_length=32, unique=True)
    desc = models.CharField(max_length=1024)

    objects = caching.base.CachingManager()

    class Meta:
        """ Metadata class for GameInfo """
        app_label = "game"
        verbose_name = "Game information"
        verbose_name_plural = "Game information"
