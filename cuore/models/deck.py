"""
Deck module
"""
from cuore.models.card import Card
from django.db import models
import caching.base


class Deck(caching.base.CachingMixin, models.Model):
    """
    Deck class
    """

    name = models.CharField(max_length=16)
    cards = models.ManyToManyField(Card)

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Deck, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Deck """
        app_label = "cuore"
        verbose_name = "Deck"
