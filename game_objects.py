# -*- coding: utf-8 -*-
"""
Module for defining blackjack game objects.

Todo:
	* Fill in method functionality
"""


class Card:
	"""
	Class to represent a card for a deck.

	Attributes:
		suit (str): One of four suits.
		rank (int): Value of card from two through ace.
	"""

	def __init__(self, suit=None, rank=None):
		"""
		Constructs attributes of card object.

		Args:
			suit (str): One of four suits.
			rank (int): Value of card from two through ace.
		"""
		self.suit = suit if suit is not None else self.get_suit()
		self.rank = rank if rank is not None else self.get_rank()

	@staticmethod
	def get_suit():
		"""
		Choose a random suit for a card.

		Returns:
			suit (str): One of four suits, randomly chosen.

		"""
		return ('spade')

	@staticmethod
	def get_rank():
		"""
		Choose a random rank for a card.

		Returns:
			rank (int): Value of card from two through ace, randomly chosen.

		"""
		return (13)


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

	card1 = Card()
	print(card1.suit, card1.rank)

	player1 = Player()
	print(player1.chips, player1.dealer)


if __name__ == '__main__':
	main()
