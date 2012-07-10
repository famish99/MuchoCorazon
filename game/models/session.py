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

    classname = models.CharField(max_length=64, editable=False, null=True)

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(DeckUser, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Overwrite the save function to save the class name for referencing
        purposes.
        """
        if not self.classname:
            cur_class = self.__class__
            class_str = cur_class.__name__
            while cur_class.__name__ != "DeckUser":
                cur_class = cur_class.__base__().__class__
                class_str = "%s.%s" % (cur_class.__name__, class_str)
            self.classname = class_str
        super(DeckUser, self). save(*args, **kwargs)

    def get_class(self):
        """
        Allow a user to query the main DeckUser table and be able to find
        the associate subclass
        """
        if self.classname == self.__class__.__name__:
            return self
        ptr = self
        for sub_class in self.classname.lower().split('.')[1:]:
            ptr = ptr.__getattribute__(sub_class)
        return ptr

    class Meta:
        """ Metadata class for Player """
        app_label = "game"
        verbose_name = "Deck User"


class Session(DeckUser):
    """
    Django model to store game state
    """

    turn = models.PositiveSmallIntegerField(null=True)
    phase = models.PositiveSmallIntegerField(null=True)

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)

    class Meta:
        """ Metadata class for Player """
        app_label = "game"
        verbose_name = "Game session"
