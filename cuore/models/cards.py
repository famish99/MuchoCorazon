from django.db import models
import caching.base


class Card(caching.base.CachinMixin, models.Model):

    name = models.CharField(max_length=32)
    image = models.ImageField(upload_to="card_images")

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)
