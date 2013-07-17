"""
Module for player models
"""
from game.models.user import UserProfile
from game.models.session import DeckUser, Session
from django.db import models
import caching.base
import uuid


class Player(DeckUser):
    """
    Django model to store player info
    """

    user = models.ForeignKey(UserProfile, related_name="players")
    session = models.ForeignKey(Session, related_name="players")

    # Used to protect json requests being made by other players
    player_key = models.CharField(max_length=32, editable=False)

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        player_key = uuid.uuid4().hex

    class Meta:
        """ Metadata class for Player """
        app_label = "game"
        verbose_name = "Player"
