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
        self.session = Session.objects.create(max_players=1)
        self.deck = Deck.objects.create(name="Sugisaki Ken's harem", user=self.session)
        self.catalog = CardCatalog.objects.create(name="Seitokai no Ichizon")

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

    def test_deck_persist(self):
        """
        Check if deck state is same after trace
        """
        self.card_list = [
                Card.objects.create(name="Sakurano Kurimu"),
                Card.objects.create(name="Akaba Chizuru"),
                Card.objects.create(name="Shiina Minatsu"),
                Card.objects.create(name="Shiina Mafuyu"),
            ]
        self.deck.insert_cards(self.card_list)
        self.deck.save()
        self.assertEqual(
                CardUser.objects.get(id=self.deck.id).get_class().card_list,
                self.deck.card_list)
