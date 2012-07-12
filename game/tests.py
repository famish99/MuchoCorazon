"""
Unit testing for the app
"""


from game.models.user import User
from game.models.player import Player
from game.models.deck import Deck
from game.models.card import CardUser, CardLibrary, Card
from game.models.session import DeckUser, Session
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


class DeckUserTestCase(TestCase):
    """
    Test associated DeckUser features
    """

    def setUp(self):
        self.user = User.objects.create(name="Sugisaki Ken")
        self.session = Session.objects.create()
        self.player = Player.objects.create(
                session=self.session, user=self.user)

    def test_class_name(self):
        """
        Check classname saving
        """
        self.assertEqual(self.player.classname, "DeckUser.Player")
        self.assertEqual(self.session.classname, "DeckUser.Session")

    def test_class_trace(self):
        """
        Check classname tracing
        """
        self.assertEqual(
                DeckUser.objects.get(id=self.player.id).get_class(),
                self.player)
        self.assertEqual(
                DeckUser.objects.get(id=self.session.id).get_class(),
                self.session)


class CardUserTestCase(TestCase):
    """
    Test associated DeckUser features
    """

    def setUp(self):
        self.session = Session.objects.create()
        self.deck = Deck.objects.create(name="hand", user=self.session)
        self.lib = CardLibrary.objects.create(name="Seitokai no Ichizon")
        self.deck.save()

    def test_class_name(self):
        """
        Check classname saving
        """
        self.assertEqual(self.deck.classname, "CardUser.Deck")
        self.assertEqual(self.lib.classname, "CardUser.CardLibrary")

    def test_class_trace(self):
        """
        Check classname tracing
        """
        self.assertEqual(
                CardUser.objects.get(id=self.deck.id).get_class(),
                self.deck)
        self.assertEqual(
                CardUser.objects.get(id=self.lib.id).get_class(),
                self.lib)


class DeckTestCase(TestCase):
    """
    Test associated Deck features
    """

    def setUp(self):
        self.session = Session.objects.create()
        self.deck = Deck.objects.create(name="Sugisaki Ken's harem", user=self.session)
        self.deck.save()
        self.card_list = [
                Card.objects.create(name="Sakurano Kurimu"),
                Card.objects.create(name="Akaba Chizuru"),
                Card.objects.create(name="Shiina Minatsu"),
                Card.objects.create(name="Shiina Mafuyu"),
            ]
        self.full_deck_str = \
            "Sugisaki Ken's harem: Sakurano Kurimu, Akaba Chizuru, Shiina Minatsu, Shiina Mafuyu"

    def test_repr(self):
        """
        Check the deck unicode representation
        """
        for card in self.card_list:
            self.deck.add_card(card)
        self.assertEqual(self.deck.__unicode__(), self.full_deck_str)

    def test_index_add_remove(self):
        """
        Check for insert/remove to index location
        """
        for card in self.card_list:
            self.deck.add_card(card)
        card = self.deck.pop_card(index=2) # Minatsu helping the baseball team
        self.assertEqual(card, self.card_list[2])
        self.deck.add_card(card, index=2) # Coming back to the harem
        self.assertEqual(self.deck.card_list, self.card_list)

    def test_push_pop(self):
        """
        Check deck push/pop
        """
        for card in self.card_list:
            self.deck.add_card(card)
        self.assertEqual(self.deck.card_list, self.card_list)
        self.card_list.reverse()
        for card in self.card_list:
            self.assertEqual(self.deck.pop_card(), card)
        for card in self.card_list:
            self.deck.add_card(card, top=False)
        self.card_list.reverse()
        for card in self.card_list:
            self.assertEqual(self.deck.pop_card(top=False), card)

    def test_enqueue_dequeue(self):
        """
        Check deck enqueue/dequeue
        """
        for card in self.card_list:
            self.deck.add_card(card, top=False)
        for card in self.card_list:
            self.assertEqual(self.deck.pop_card(), card)
        for card in self.card_list:
            self.deck.add_card(card)
        for card in self.card_list:
            self.assertEqual(self.deck.pop_card(top=False), card)

    def test_shuffle(self):
        """
        Test validity of shuffle
        """
        for card in self.card_list:
            self.deck.add_card(card)
        self.assertEqual(self.deck.card_list, self.card_list)
        self.deck.shuffle()
        self.assertNotEqual(self.deck.card_list, self.card_list)
