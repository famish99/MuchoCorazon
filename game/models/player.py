"""
Module for player models
"""
from game.models.session import DeckUser, Session
from django.db import models
import caching.base


class Player(DeckUser):
    """
    Django model to store player info
    """

    session = models.ForeignKey(Session, related_name="players")

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Player """
        app_label = "game"
        verbose_name = "Player"
