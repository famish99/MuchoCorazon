"""
Card module containing the basic card classes.
The actual cards played will be derived from these.
"""


class Card:
	"""
	Basic card class
	"""

	employ_cost = None
	card_name = None
	serving_cost = None


class LoveCard(Card):
	"""
	Love giving card
	"""

	love_count = None
	serving_cost = 0


class OneLoveCard(LoveCard):
	"""
	1 Love giving card
	"""

	love_count = 1
	employ_cost = 1
	card_name = "1 Love"


class TwoLoveCard(LoveCard):
	"""
	2 Love giving card
	"""

	love_count = 2
	employ_cost = 4
	card_name = "2 Love"


class ThreeLoveCard(LoveCard):
	"""
	3 Love giving card
	"""

	love_count = 3
	employ_cost = 7
	card_name = "3 Love"


class EventCard(EventCard):
	"""
	Base class for Illness/Bad Habits
	"""

	victory_point = None


class Illness(EventCard):
	"""
	Illness card
	"""

	victory_point = 0
	employ_cost = 4
	card_name = "Illness"


class BadHabit(EventCard):
	"""
	Bad Habit Card
	"""

	victory_point = -1
	employ_cost = 2
	card_name = "Bad Habit"


class MaidCard(Card):
	"""
	Base Maid card
	"""

	love_count = None
	victory_point = None
