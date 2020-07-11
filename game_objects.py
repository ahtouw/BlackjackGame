# -*- coding: utf-8 -*-
"""
Module for defining blackjack game objects.

Todo:
	* Fill in method functionality
"""
import random

class Card:
	"""
	Class to represent a card for a deck.

	Attributes:
		suit (str): One of four suits.
		rank (str): Value of card from two through ace.
	"""
	suits = ["clubs", "diamonds", "hearts", "spades"]
	ranks = [None, "ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]

	def __init__(self, suit=None, rank=None):
		"""
		Constructs attributes of card object.

		Args:
			suit (str): One of four suits.
			rank (str): Value of card from two through ace.
		"""
		# random_suit/rank is DANGEROUS. Needs fix.
		self.suit = suit if suit is not None and suit in self.suits else self.random_suit()
		self.rank = rank if rank is not None and rank in self.ranks else self.random_rank()

	def __str__(self):
		"""
		Returns:
			str: Readable version of card.
		"""
		return (self.rank + " of " + self.suit)

	@staticmethod
	def random_suit():
		"""
		Choose a random suit for a card.

		Returns:
			suit (str): One of four suits, randomly chosen.

		"""
		return random.choice(Card.suits)

	@staticmethod
	def random_rank():
		"""
		Choose a random rank for a card.

		Returns:
			rank (str): Value of card from two through ace, randomly chosen.

		"""
		return random.choice(Card.ranks[1:])


class Player:
	"""
	Class to represent a blackjack player.

	Attributes:
		dealer (bool): Specifies whether player is dealer.
		chips (int): Currency of game player can use to bet. None if dealer.
		hand: Cards that player possesses.
	"""

	def __init__(self, dealer=None, chips=50_000, hand=None):
		"""
		Constructs attributes of player object.

		Args:
			dealer (bool): Specifies whether player is dealer.
			chips (int): Currency of game player can use to bet. None if dealer.
			hand: Cards that player possesses.
		"""
		self.dealer = dealer if dealer is not None else False
		self.chips = chips if not self.dealer else None
		self.hand = hand if hand is not None else False
# if not self.dealer:
# 	if chips is not None:
# 		self.chips = chips
# 	else:
# 		self.chips = 0


def main():
	"""Executes Blackjack game and concludes run."""

	card1 = Card(rank="422",suit="diamonds")
	print(card1)

	player1 = Player()
	print(player1.chips, player1.dealer)


if __name__ == '__main__':
	main()
