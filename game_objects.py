# -*- coding: utf-8 -*-
"""
Module for defining blackjack game objects.

Todo:
	* Figure out how to implement reward system for double/split
	* Work out how to implement split new hand
"""
import random
from math import floor


class Card:
	"""
	Class to represent a card for a deck.

	Attributes:
		suit (str): One of four suits.
		rank (str): Value of card from two through ace.
	"""
	suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
	ranks = [None, "Ace", "Two", "Three", "Four", "Five", "Six",
	         "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]

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
		return self.rank + " of " + self.suit

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


class Hand:
	"""
	Uses Card class to construct deck object.

	Attributes:
		name (str): Name of player.
		dealer (bool): Specifies whether player is dealer.
	"""

	def __init__(self, name, dealer=False, hand=None):
		"""
		Constructs attributes of Hand object.

		Args:
			name (str): Name of player.
			dealer (bool): Specifies whether player is dealer.
			hand (list): Group of cards.
		"""
		self.name = name
		self.dealer = dealer
		self.hand = hand if hand is not None else []
		self.size = self.set_size()
		self.double_down = False
		self.score = None

	def set_size(self):
		"""
		Find the hand size.

		Returns:
			int : length of hand.
		"""
		self.size = len(self.hand)

	def draw_card(self, deck):
		"""
		Draws card from deck and adds to hand.

		Args:
			deck (Deck): From Deck class.

		Returns:
			None
		"""
		card = deck.deal_card()
		self.hand.append(card)
		self.set_size()
		self.score = self.set_score()

	def deal_hand(self, deck, hand_size):
		while len(self.hand) < hand_size:
			self.draw_card(deck)

	def set_score(self):
		"""
		Should ONLY be used in draw_card method.

		Returns:
			int : Score of hand.
		"""
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

	def has_blackjack(self):
		"""
		Checks if a two-card blackjack was dealt

		Returns:
			bool : True if blackjack dealt.
		"""
		if len(self.hand) == 2 and self.score == 21:
			return True
		else:
			return False

	def print_hand(self, show_dealer=False):
		"""
		Prints hand contents.

		Returns:
			None
		"""
		print(f"\n{self.name}'s cards: ")
		if not self.dealer or show_dealer:
			print(f"Total {self.score}")
		print("---------------------------")
		for dealt_cards, card in enumerate(self.hand, 1):
			if self.dealer and dealt_cards == 1 and not show_dealer:
				print("Hidden card")
			else:
				if card.ace:
					print(f"{str(card):<20} (1/11)")
				else:
					print(f"{str(card):<20} ({card.rank_value()})")
		print("---------------------------")

	def reset_hand(self):
		"""
		Resets hand to empty list.

		Returns:
			None
		"""
		self.hand = []
		self.set_size()
		self.set_score()
		self.double_down = False


class Player:
	"""
	Class to represent a blackjack player.

	Attributes:
		dealer (bool): Specifies whether player is dealer.
		chips (int): Currency of game player can use to bet. None if dealer.
		hands (list): Hands that player possesses.
	"""

	def __init__(self, dealer=None, chips=50_000, hands=None, name="Player"):
		"""
		Constructs attributes of Player object.

		Args:
			dealer (bool): Specifies whether player is dealer.
			chips (int): Currency of game player can use to bet. None if dealer.
			hands (list): Hands that player possesses.
			name (str): Name of player.
		"""
		self.name = "Dealer" if dealer else name
		self.dealer = dealer if dealer is not None else False
		self.chips = chips if not self.dealer else None
		self.hands = hands if hands is not None else [Hand(self.name, self.dealer)]  # Filled with Card objects
		self.current_hand = self.hands[0]
		self.bet = None

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
				self.bet = int(input("Place your bet: "))
			except ValueError:
				print("Must be a whole number! Try again.")
				continue
			else:
				if self.bet > self.chips:
					print(f"Not enough chips remaining. Try again.")
					continue
				elif self.bet <= 0:
					print(f"Invalid bet. Try again.")
					continue
				else:
					self.place_bet()
					break

	def place_bet(self):
		"""
		Places specified bet and increments bet_count.

		Returns:
			None
		"""
		self.chips -= self.bet

	def get_move(self, deck):
		"""
		Get user input for move to play. Implements blackjack rules.

		Notes:
			2-card BJ already accounted for in Blackjack method 'take_turns'.

		Args:
			deck (Deck): From Deck class.

		Returns:
			turn_over (bool): Whether or not player's turn ends.
		"""
		turn_over = True
		double = False
		split = False
		if self.current_hand.has_blackjack():
			return turn_over
		while True:
			try:
				print()
				if self.current_hand.size == 2 and self.bet < self.chips:  # double
					double = True
					if self.current_hand.hand[0].rank == self.current_hand.hand[1].rank:  # split
						split = True
						move_selection = int(input("Hit, Stand, Double, or Split (1, 3, 5, 7): "))
					else:
						move_selection = int(input("Hit, Stand, or Double (1, 3, 5): "))
				else:
					move_selection = int(input("Hit or Stand (1 or 3): "))
			except ValueError:
				print("Must be a whole number! Try again.")
				continue
			else:
				if move_selection == 1:
					self.current_hand.draw_card(deck)
					print("Here's your card: ")
					if self.current_hand.score > 21:
						return turn_over
					else:
						return not turn_over
				elif move_selection == 3:
					print("Stand.")
					return turn_over
				elif move_selection == 5 and double:
					self.place_bet()
					self.current_hand.double_down = True
					print(f"Chips remaining: {self.chips}")
					self.current_hand.draw_card(deck)
					print("Here's your card: ")
					return turn_over
				elif move_selection == 7 and split:
					self.split_hand(deck)
					return turn_over
				else:
					print("Invalid input. Try again.")
					continue

	def split_hand(self, deck):
		"""
		Implements hand split.

		Returns:
			None
		"""
		self.place_bet()
		split_hand = Hand(name=self.current_hand.name, hand=[self.current_hand.hand.pop()])
		split_hand.draw_card(deck)
		self.current_hand.draw_card(deck)
		self.hands.append(split_hand)
		for _ in range(0, 2):
			turn_over = False
			self.current_hand.print_hand()
			while not turn_over:
				turn_over = self.get_move(deck)
				self.current_hand.print_hand()
			self.current_hand = split_hand

	def award_chips(self, result):
		"""
		Uses blackjack results to alter chips

		Args:
			result (str): Result of blackjack hand.

		Returns:
			None
		"""
		if result == "blackjack":
			self.chips += floor(self.bet * 2.5)
		elif result == "win":
			if self.current_hand.double_down:
				self.chips += self.bet * 2 * 2
			else:
				self.chips += self.bet * 2
		elif result == "push":
			if self.current_hand.double_down:
				self.chips += self.bet * 2
			else:
				self.chips += self.bet
		else:
			raise ValueError(f"Input '{result}' invalid, expected 'blackjack', 'win', or 'push'.")

	def reset_hands(self):
		"""
		Resets hand to empty list.

		Returns:
			None
		"""
		self.current_hand.reset_hand()
		self.hands = [self.current_hand]
		self.bet = 0


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
