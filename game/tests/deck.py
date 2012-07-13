"""
Deck unit testing
"""
from game.models.deck import Deck
from game.models.session import Session
from game.models.card import Card
from django.test import TestCase
import copy


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
            "Sugisaki Ken's harem: Shiina Mafuyu, Shiina Minatsu, Akaba Chizuru, Sakurano Kurimu"

    def test_repr(self):
        """
        Check the deck unicode representation
        """
        for card in self.card_list:
            self.deck.insert_card(card)
        self.assertEqual(self.deck.__unicode__(), self.full_deck_str)

    def test_push_pop(self):
        """
        Check deck push/pop
        """
        for card in self.card_list:
            self.deck.insert_card(card)
        self.card_list.reverse()
        self.assertEqual(self.deck.card_list, self.card_list)
        for card in self.card_list:
            self.assertEqual(self.deck.remove_card(), card)
        for card in self.card_list:
            self.deck.insert_card(card, top=False)
        self.card_list.reverse()
        for card in self.card_list:
            self.assertEqual(self.deck.remove_card(top=False), card)

    def test_enqueue_dequeue(self):
        """
        Check deck enqueue/dequeue
        """
        for card in self.card_list:
            self.deck.insert_card(card, top=False)
        for card in self.card_list:
            self.assertEqual(self.deck.remove_card(), card)
        for card in self.card_list:
            self.deck.insert_card(card)
        for card in self.card_list:
            self.assertEqual(self.deck.remove_card(top=False), card)

    def test_shuffle(self):
        """
        Test validity of shuffle
        """
        for card in self.card_list:
            self.deck.insert_card(card)
        self.card_list.reverse()
        self.assertEqual(self.deck.card_list, self.card_list)
        self.deck.shuffle()
        self.assertNotEqual(self.deck.card_list, self.card_list)

    def test_index_add_remove(self):
        """
        Check for insert/remove to index location
        """
        for card in self.card_list:
            self.deck.insert_card(card)
        card = self.deck.remove_card(index=1) # Minatsu helping the baseball team
        self.assertEqual(card, self.card_list[2])
        self.deck.insert_card(card, index=1) # Coming back to the harem
        self.card_list.reverse()
        self.assertEqual(self.deck.card_list, self.card_list)

    def test_multi_add_remove(self):
        """
        Check ability to insert/remove multiple cards at once
        """
        rev_list = copy.copy(self.card_list)
        rev_list.reverse()
        # Test adding all the cards
        self.deck.insert_cards(self.card_list)
        self.assertEqual(self.deck.card_list, rev_list)
        # Test removing all cards in stack fashion
        ret_deck = self.deck.remove_cards(len(self.card_list))
        self.assertEqual(self.deck.card_list, [])
        ret_deck.reverse()
        self.assertEqual(ret_deck, self.card_list)
        # Test removing in a queue fashion
        self.deck.insert_cards(self.card_list)
        ret_deck = self.deck.remove_cards(len(self.card_list), top=False)
        self.assertEqual(ret_deck, self.card_list)
        # Test removing back half
        self.deck.insert_cards(self.card_list)
        self.deck.remove_cards(2, index=2)
        self.assertEqual(self.deck.card_list, rev_list[0:2])
        # Reinsert cards into middle
        self.deck.insert_cards(self.card_list[0:2], index=1)
        check_list = [
                self.card_list[3],
                self.card_list[1],
                self.card_list[0],
                self.card_list[2],
                ]
        self.assertEqual(self.deck.card_list, check_list)
