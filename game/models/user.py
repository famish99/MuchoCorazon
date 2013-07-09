"""
Module for user models
"""
from django.contrib.auth.models import User
from django.db import models
import caching.base


class UserProfile(caching.base.CachingMixin, models.Model):
    """
    Django model to store user info
    """

    user = models.OneToOneField(User, related_name="profile")

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Player """
        app_label = "game"
        verbose_name = "User Profile"
