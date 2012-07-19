"""
Session models unit testing
"""
from django.contrib.auth.models import User
from game.models.session import DeckUser, Session
from game.models.user import UserProfile
from django.test import TestCase
from game.models.player import Player


class DeckUserTestCase(TestCase):
    """
    Test associated DeckUser features
    """

    def setUp(self):
        test_user = User.objects.create(first_name="Ken", last_name="Sugisaki")
        self.user = UserProfile.objects.create(user=test_user)
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


class SessionTestCase(TestCase):
    """
    Test associated Session features
    """

    def setUp(self):
        name_list = [
                "Sugisaki_Ken",
                "Echo_of_Death",
                "Nakameguro",
                ]
        self.user_list = []
        self.player_list = []
        self.session = Session.objects.create()
        for name in name_list:
            test_user = User.objects.create(username=name)
            self.user_list.append(UserProfile.objects.create(user=test_user))

    def test_next_turn(self):
        """
        Test next turn method
        """
        for user in self.user_list:
            self.player_list.append(self.session.add_player(user))
        self.assertEqual(self.session.turn, 0)
        self.session.next_turn()
        self.assertEqual(self.session.turn, 1)
        self.session.next_turn()
        self.assertEqual(self.session.turn, 2)
        self.session.next_turn()
        self.assertEqual(self.session.turn, 0)

    def test_add_remove_player(self):
        """
        Test add/remove players to session
        """
        for user in self.user_list:
            self.player_list.append(self.session.add_player(user))
        self.assertEqual(self.session.player_list, self.player_list)
        # Make sure you can't add player to existing seat
        self.assertRaises(
                ValueError,
                self.session.add_player, self.user_list[0], index=2)
        self.assertEqual(
                self.session.remove_player(index=1), self.player_list[1])
        check_list = [
                self.player_list[0],
                None,
                self.player_list[2]
                ]
        self.assertEqual(self.session.player_list, check_list)

    def test_shuffle(self):
        """
        Test shuffling players around
        """
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
                ]
        self.assertEqual(self.session.player_list, check_list)
