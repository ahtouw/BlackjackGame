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
	suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
	ranks = [None, "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

	def __init__(self, suit=None, rank=None):
		"""
		Constructs attributes of Card object.

		Args:
			suit (str): One of four suits.
			rank (str): Value of card from two through ace.
		"""
		# random_suit/rank is DANGEROUS. Needs fix.
		self.suit = suit if suit is not None and suit in self.suits else self.random_suit()
		self.rank = rank if rank is not None and rank in self.ranks else self.random_rank()
		self.ace = True if self.rank == "Ace" else False

	def __str__(self):
		"""

		Returns:
			str: Readable version of card.
		"""
		return (self.rank + " of " + self.suit)

	def rank_value(self):
		"""
		Converts rank to blackjack values.

		Returns:
			int : Value of rank.
		"""
		rank_val = Card.ranks.index(self.rank)
		if self.ace:
			return 11
		elif rank_val <= 10:
			return rank_val
		else:
			return 10

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


class Deck:
	"""
	Uses Card class to construct deck object.

	Attributes:
		decks (int): Number of decks of cards.
	"""

	def __init__(self, decks=8):
		"""
		Constructs attributes of Deck object.

		Args:
			decks (int): Number of decks of cards.
		"""
		self.decks = decks
		self.card_stack = self.build_stack()
		self.STACK_COUNT = self.remaining_cards()
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

	def shuffle_check(self, shuffle_percent):
		"""
		Checks if card_stack has below a specified percentage of cards left.

		Args:
			shuffle_percent (float): When card_stack has more than this percent of cards missing, shuffle.
		Returns:
			None
		"""
		percent_left = 1 - self.remaining_cards() / self.STACK_COUNT
		if percent_left > shuffle_percent:
			self.card_stack = self.build_stack()
			self.shuffle()
			print()
			print("Shuffling. . . ")

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

	def __init__(self, dealer=None, chips=50_000, hand=None, lost=None, name="Player"):
		"""
		Constructs attributes of Player object.

		Args:
			dealer (bool): Specifies whether player is dealer.
			chips (int): Currency of game player can use to bet. None if dealer.
			hand (list): Cards that player possesses.
			lost (bool): Whether the player lost the hand.
			name (str): Name of player.
		"""
		self.dealer = dealer if dealer is not None else False
		self.chips = chips if not self.dealer else None
		self.hand = hand if hand is not None else []  # Filled with Card objects
		self.name = "Dealer" if dealer else name
		self.bet = None
		self.lost = lost if lost is not None else False

	def draw_card(self, deck):
		"""
		Draws card from deck and adds to hand.

		Args:
			deck (object): From Deck class.

		Returns:
			None
		"""
		card = deck.deal_card()
		self.hand.append(card)

	def get_bet(self):
		"""
		Get user input, only accepts integers. Checks remaining chips

		Returns:
			int : Valid bet.
		"""
		while True:
			try:
				print()
				print(f"{self.name}, you have {self.chips} chips.")
				bet = int(input("Place your bet: "))
			except ValueError:
				print("Must be a whole number! Try again.")
				continue
			else:
				if bet > self.chips:
					print(f"Not enough chips remaining. Try again.")
					continue
				elif bet <= 0:
					print(f"Invalid bet. Try again.")
					continue
				else:
					self.bet = bet
					self.chips -= bet
					break

	def get_move(self, deck):
		"""
		Get user input for move to play. Implements blackjack rules
		Args:
			deck (object): From Deck class.

		Returns:
			bool : Whether or not player's turn ends.
		"""
		# first_move = True
		while True:
			try:
				print()
				move_selection = int(input("Hit or Stand (1 or 3): "))
			except ValueError:
				print("Must be a whole number! Try again.")
				continue
			else:
				if move_selection == 1:
					print("Here's your card: ")
					self.draw_card(deck)
					if self.hand_total() > 21:
						self.lost = True
						return True
					else:
						return False
				elif move_selection == 3:
					print("Stand.")
					return True
				else:
					print("Invalid input. Try again.")
					continue

	def hand_total(self):
		total = 0
		ace_count = 0
		if self.hand:
			for card in self.hand:
				total += card.rank_value()
				if card.ace:
					ace_count += 1
			while total > 21 and ace_count >= 1:
				total -= 10
				ace_count -= 1
		return total

	def print_hand(self, show_dealer=False):
		"""
		Prints hand contents.

		Returns:
			None
		"""
		print()
		print(f"{self.name} cards: ")
		if not self.dealer or show_dealer:
			print(f"Total {self.hand_total()}")
		print("--------------")
		for dealt_cards, card in enumerate(self.hand, 1):
			if self.dealer and dealt_cards == 1 and not show_dealer:
				print("Hidden card")
			else:
				print(card, f" ({card.rank_value()})")
		print("--------------")

	def reset_hand(self):
		"""
		Resets hand to empty list.

		Returns:
			None
		"""
		self.hand = []


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
