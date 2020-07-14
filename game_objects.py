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
	ranks = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]

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
		return random.choice(Card.ranks)


class Deck:
	"""
	Uses Card class to construct deck object.

	Attributes:
		decks (int): Number of decks of cards.
	"""

	def __init__(self, decks=8):
		"""
		Constructs attributes of deck object.

		Args:
			decks (int): Number of decks of cards.
		"""
		self.decks = decks
		self.card_stack = self.build_stack()
		self.shuffle()

	def build_stack(self):
		"""
		Builds card_stack based on number of decks input.

		Returns:
			card_stack (list)
		"""
		card_stack = []
		for _ in range(self.decks):
			for suit in Card.suits:
				for rank in Card.ranks:
					card_stack.append(Card(rank=rank, suit=suit))
		return card_stack

	def shuffle(self):
		"""
		Shuffles card_stack.

		Returns:
			None
		"""
		random.shuffle(self.card_stack)

	def deal_card(self):
		"""
		Removes a card from the top off the deck.

		Returns:
			card (str): Card removed from deck.
		"""
		return self.card_stack.pop()

	def remaining_cards(self):
		"""
		Shows how many card are left in card_stack.
		Returns:
			int : Number of cards in card_stack
		"""
		return len(self.card_stack)

	def print_stack(self):
		"""
		Prints card_stack contents.

		Returns:
			None
		"""
		for card in self.card_stack:
			print(card)


class Player:
	"""
	Class to represent a blackjack player.

	Attributes:
		dealer (bool): Specifies whether player is dealer.
		chips (int): Currency of game player can use to bet. None if dealer.
		hand: Cards that player possesses.
	"""

	def __init__(self, dealer=None, chips=50_000, hand=None, name="Player"):
		"""
		Constructs attributes of player object.

		Args:
			dealer (bool): Specifies whether player is dealer.
			chips (int): Currency of game player can use to bet. None if dealer.
			hand: Cards that player possesses.
		"""
		self.dealer = dealer if dealer is not None else False
		self.chips = chips if not self.dealer else None
		self.hand = hand if hand is not None else []
		self.name = "Dealer" if dealer else name

	def print_hand(self):
		"""
		Prints hand contents.

		Returns:
			None
		"""
		for counter, card in enumerate(self.hand, 1):
			print()
			print(f"{self.name} card {counter}: ")
			if self.dealer and counter == 1:
				print("Hidden Dealer card")
			else:
				print(card)


def main():
	"""Executes Blackjack game and concludes run."""

	deck1 = Deck(decks=2)
	deck1.print_stack()

	print("---------")
	print(deck1.deal_card())
	deck1.deal_card()
	print("---------")
	deck1.print_stack()
	print(deck1.remaining_cards())


if __name__ == '__main__':
	main()
