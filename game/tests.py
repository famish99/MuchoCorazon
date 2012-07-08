"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from game.models.user import User
from game.models.player import Player
from game.models.session import DeckUser, Session
from django.test import TestCase


class DeckUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Sugisaki Ken")
        self.session = Session.objects.create(turn=0, phase=0)
        self.player = Player.objects.create(
                session=self.session, user=self.user)

    def test_classname(self):
        """ Check classname saving """
        self.assertEqual(self.player.classname, "DeckUser.Player")
        self.assertEqual(self.session.classname, "DeckUser.Session")
