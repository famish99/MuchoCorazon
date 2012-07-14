"""
Card models unit testing
"""
from game.models.card import CardUser, CardCatalog, Card
from game.models.deck import Deck
from game.models.session import Session
from django.test import TestCase


class CardTestCase(TestCase):
    """
    Tests associated Card features
    """

    def setUp(self):
        self.card = Card.objects.create(name="Shiina Minatsu")

    def test_repr(self):
        """
        Check unicode representation
        """
        self.assertEqual(self.card.__unicode__(), "Shiina Minatsu")

class CardCatalogTestCase(TestCase):
    """
    Tests associated 
    """

class CardUserTestCase(TestCase):
    """
    Test associated DeckUser features
    """

    def setUp(self):
        self.session = Session.objects.create()
        self.deck = Deck.objects.create(name="hand", user=self.session)
        self.catalog = CardCatalog.objects.create(name="Seitokai no Ichizon")
        self.deck.save()

    def test_class_name(self):
        """
        Check classname saving
        """
        self.assertEqual(self.deck.classname, "CardUser.Deck")
        self.assertEqual(self.catalog.classname, "CardUser.CardCatalog")

    def test_class_trace(self):
        """
        Check classname tracing
        """
        self.assertEqual(
                CardUser.objects.get(id=self.deck.id).get_class(),
                self.deck)
        self.assertEqual(
                CardUser.objects.get(id=self.catalog.id).get_class(),
                self.catalog)

