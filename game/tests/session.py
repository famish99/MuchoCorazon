"""
Session models unit testing
"""
from django.contrib.auth.models import User
from django.utils.datastructures import SortedDict
from game.models.session import DeckUser, Session
from game.models.user import UserProfile
from game.models.card import Card
from django.test import TestCase
from game.models.player import Player


class DeckUserTestCase(TestCase):
    """
    Test associated DeckUser features
    """

    def setUp(self):
        self.test_data = SortedDict([
                ("FF8", [
                    Card.objects.create(name="Laguna Loire"),
                    Card.objects.create(name="Quistis Trepe"),
                    Card.objects.create(name="Irvine Kinneas"),
                    ]),
                ("FF9", [
                    Card.objects.create(name="Vivi"),
                    Card.objects.create(name="Garnet"),
                    Card.objects.create(name="Eiko"),
                    ]),
                ("FF12", [
                    Card.objects.create(name="Vaan"),
                    Card.objects.create(name="Ashe"),
                    Card.objects.create(name="Bathier"),
                    ]),
                ])
        test_user = User.objects.create(username="final_fantasy")
        self.user = UserProfile.objects.create(user=test_user)
        self.session = Session.objects.create(max_players=1)
        self.player = Player.objects.create(
                session=self.session, user=self.user)

    def test_add_deck(self):
        """
        Test deck adding
        """
        deck_list = []
        for name in self.test_data.keys():
            deck_list.append((name, self.player.add_deck(name)))
        player_decks = self.player.deck_list
        for deck in deck_list:
            self.assertEqual(player_decks.get(deck[0]), deck[1])

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

    def test_draw_card(self):
        """
        Check draw engine
        """
        deck_list = []
        for deck_name, cards in self.test_data.items():
            deck = self.player.add_deck(deck_name)
            deck_list.append(deck)
            deck.insert_cards(cards)
        deck_0 = self.test_data.values()[0][::-1]
        deck_1 = self.test_data.values()[1][::-1]
        deck_2 = self.test_data.values()[2][::-1]
        DeckUser.draw_cards(deck_list[0], deck_list[1])
        self.assertEqual(deck_list[0].card_list, deck_0[1:])
        self.assertEqual(deck_list[1].card_list, [deck_0[0]] + deck_1)
        DeckUser.draw_cards(deck_list[0], deck_list[1], num_cards=2)
        self.assertEqual(deck_list[0].card_list, [])
        self.assertEqual(deck_list[1].card_list, deck_0[::-1] + deck_1)
        DeckUser.draw_cards(deck_list[2], deck_list[1], all=True)
        self.assertEqual(deck_list[2].card_list, [])
        self.assertEqual(deck_list[1].card_list, deck_2[::-1] + deck_0[::-1] + deck_1)


class SessionTestCase(TestCase):
    """
    Test associated Session features
    """

    def setUp(self):
        name_list = [
                "Senjougahara Hitagi",
                "Hachikuji Mayoi",
                "Kanbaru Suruga",
                "Sengoku Nadeko",
                "Hanekawa Tsubasa",
                ]
        self.user_list = []
        self.player_list = []
        self.session = Session.objects.create(name="test_name", max_players=len(name_list))
        for name in name_list:
            test_user = User.objects.create(username=name)
            self.user_list.append(UserProfile.objects.create(user=test_user))

    def test_phase_methods(self):
        """
        Test phase methods
        """
        phase_list = [
                "Hitagi Crab",
                "Mayoi Snail",
                "Suruga Monkey",
                "Nadeko Snake",
                "Tsubasa Cat",
                ]
        for phase in phase_list:
            self.session.add_phase(phase)
        self.assertEqual(phase_list, self.session.phase_list)
        self.assertEqual(self.session.current_phase(), phase_list[0])
        self.session.next_phase()
        self.assertEqual(self.session.current_phase(), phase_list[1])
        self.session.next_phase()
        self.assertEqual(self.session.current_phase(), phase_list[2])
        self.session.next_phase()
        self.assertEqual(self.session.current_phase(), phase_list[3])
        self.session.next_phase()
        self.assertEqual(self.session.current_phase(), phase_list[4])
        self.session.next_phase()
        self.assertEqual(self.session.current_phase(), phase_list[0])
        self.assertEqual(self.session.turn, 1)

    def test_turn_methods(self):
        """
        Test turn methods
        """
        for user in self.user_list:
            self.player_list.append(self.session.add_player(user))
        self.assertEqual(self.session.turn, 0)
        self.assertEqual(self.session.current_player(), self.player_list[0])
        self.session.next_turn()
        self.assertEqual(self.session.turn, 1)
        self.assertEqual(self.session.current_player(), self.player_list[1])
        self.session.next_turn()
        self.assertEqual(self.session.turn, 2)
        self.assertEqual(self.session.current_player(), self.player_list[2])
        self.session.next_turn()
        self.assertEqual(self.session.turn, 3)
        self.assertEqual(self.session.current_player(), self.player_list[3])
        self.session.next_turn()
        self.assertEqual(self.session.turn, 4)
        self.assertEqual(self.session.current_player(), self.player_list[4])
        self.session.next_turn()
        self.assertEqual(self.session.turn, 5)
        self.assertEqual(self.session.current_player(), self.player_list[0])

    def test_add_remove_player(self):
        """
        Test add/remove players to session
        """
        for user in self.user_list:
            self.player_list.append(self.session.add_player(user))
        self.assertEqual(self.session.player_list, self.player_list)
        # Test for max_players sanity checking
        self.assertRaises(
                ValueError,
                self.session.add_player, self.user_list[0])
        self.assertEqual(
                self.session.remove_player(index=1), self.player_list[1])
        # Make sure you can't add player to existing seat
        self.assertRaises(
                ValueError,
                self.session.add_player, self.user_list[0], index=2)
        check_list = [
                self.player_list[0],
                None,
                self.player_list[2],
                self.player_list[3],
                self.player_list[4],
                ]
        self.assertEqual(self.session.player_list, check_list)

    def test_num_players(self):
        for user in self.user_list:
            self.player_list.append(self.session.add_player(user))
        self.assertEqual(self.session.num_players, len(self.player_list))

    def test_shuffle(self):
        """
        Test shuffling players around
        """
        self.session = Session.objects.create(name="test_name", max_players=10*len(self.user_list))
        for user in self.user_list*10:
            self.player_list.append(self.session.add_player(user))
        self.session.shuffle_players()
        self.assertNotEqual(self.session.player_list, self.player_list)
    
    def test_swap(self):
        """
        Test swapping two players around
        """
        for user in self.user_list:
            self.player_list.append(self.session.add_player(user))
        self.session.swap_players(1, 2)
        check_list = [
                self.player_list[0],
                self.player_list[2],
                self.player_list[1],
                self.player_list[3],
                self.player_list[4],
                ]
        self.assertEqual(self.session.player_list, check_list)
