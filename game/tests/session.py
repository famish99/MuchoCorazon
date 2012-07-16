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
