"""
Module for user models
"""
from django.db import models
import caching.base


class User(caching.base.CachingMixin, models.Model):
    """
    Django model to store user info
    """

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Player """
        app_label = "cuore"
        verbose_name = "User info"
