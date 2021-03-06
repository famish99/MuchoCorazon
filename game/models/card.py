"""
Module containing the card model
"""
from django.db import models
from picklefield.fields import PickledObjectField
import caching.base


class CardUser(caching.base.CachingMixin, models.Model):
    """
    Class to get around the limitation that Card can't be ForeignKey'd
    to either Deck or CardLibrary
    """

    classname = models.CharField(max_length=64, editable=False, null=True)

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(CardUser, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Overwrite the save function to save the class name for referencing
        purposes.
        """
        if not self.classname:
            cur_class = self.__class__
            class_str = cur_class.__name__
            while cur_class.__name__ != "CardUser":
                cur_class = cur_class.__base__().__class__
                class_str = "%s.%s" % (cur_class.__name__, class_str)
            self.classname = class_str
        super(CardUser, self). save(*args, **kwargs)

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
        """ Metadata class for CardUser """
        app_label = "game"
        verbose_name = "Card User"


class CardCatalog(CardUser):
    """
    For a whole game module, store all the cards it has available.
    This should not be instantiated for each game session, but only
    when a new game module is added e.g. Tanto Cuore, Magic the Gathering,
    Poker, etc.


    -determines what cards get instantiated when game starts
    """

    name = models.CharField(max_length=32)
    _card_dict = PickledObjectField()

    def __init__(self, *args, **kwargs):
        super(CardUser, self).__init__(*args, **kwargs)
        self._card_dict = {}

    def load_catalog(self, card_module):
        """
        Load cards from module into database
        """
        from card_module import CARD_LIST
        
        for card in CARD_LIST:
            pass

    class Meta:
        """ Metadata class for CardCatalog """
        app_label = "game"
        verbose_name = "Card Catalog"


class Card(caching.base.CachingMixin, models.Model):
    """
    Django model to store a single card
    """

    deck = models.ForeignKey(CardUser, related_name="cards", null=True)
    name = models.CharField(max_length=32)
    image = models.ImageField(upload_to="card_images")

    objects = caching.base.CachingManager()

    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        """ Metadata class for Card """
        app_label = "game"
        verbose_name = "Card"
