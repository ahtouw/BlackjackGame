# -*- coding: utf-8 -*-
"""
Module for creating blackjack game.

Todo:
	* Fix rule system, winning/losing
	* Add double, split functions
	* Add Blackjack deal
"""
from math import floor

from game_objects import Deck, Player


class Blackjack:
	"""
	Class to make and run game.

	Attributes:
		player_list (list): All active players.
		dealer (object): From Player class.
		deck (object): From Deck class.
	"""

	def __init__(self):
		"""
		Constructs attributes of Blackjack object.

		Args:
			player_list (list): All active players.
			deck (object): From Deck class.
		"""
		self.player_list = [Player(name="Frank"), Player(name="Jane")]
		self.dealer = Player(dealer=True)
		self.deck = Deck(decks=1)

	def run(self):
		"""
		Runs blackjack game until player exits.

		Returns:
			None
		"""
		playing = True
		self.game_message("Welcome")
		while playing:
			self.take_bets()
			self.deal_hands()
			self.take_turns()
			self.clear_table()

			self.deck.shuffle_check(.70)
			self.game_message("Play again!")
			print("\nNext round starting. . .")
			if input("\nPress 'x' to leave the table: ") == "x":
				playing = False

	def take_bets(self):
		"""
		Takes bets for all players.

		Returns:
			None
		"""
		for player in self.player_list:
			player.get_bet()
			print(f"Chips remaining: {player.chips}")

	def deal_hands(self):
		"""
		Deals hand to all players.

		Returns:
			None
		"""
		for card_num in range(1, 3):
			for player in self.player_list:
				player.draw_card(self.deck)
			self.dealer.draw_card(self.deck)

	def take_turns(self):
		"""
		Takes turn for all players including dealer

		Returns:
			None
		"""
		for player in self.player_list:
			turn_over = False
			self.game_message(player.name + "'s turn")
			player.print_hand()
			while not turn_over:
				self.dealer.print_hand(show_dealer=False)
				if player.has_blackjack() and not self.dealer.has_blackjack():
					self.find_winner(blackjack_winner=player)
					break
				turn_over = player.get_move(self.deck)
				player.print_hand()

		self.game_message("Results")
		while self.dealer.hand_total() < 17:
			self.dealer.print_hand(show_dealer=True)
			self.dealer.draw_card(self.deck)
		self.dealer.print_hand(show_dealer=True)

		self.find_winner()

	def find_winner(self, blackjack_winner=None):
		"""
		Evaluates if player or dealer won hand.

		Args:
			blackjack_winner (object): Player with blackjack
		Returns:
			None
		"""
		if blackjack_winner:
			print()
			print("-- ---- BLACKJACK WINNER!!! ---- --")
			blackjack_winner.chips += floor(blackjack_winner.bet * 2.5)
			print(f"{blackjack_winner.name} chips: {blackjack_winner.chips}")
		else:
			for player in self.player_list:
				if player.has_blackjack():
					continue
				player.print_hand()
				print()
				if self.dealer.hand_total() > 21 and not player.lost:
					print("BUST! House loses!")
					print(f"{player.name} wins!")
					player.chips += player.bet * 2
				elif self.dealer.hand_total() > player.hand_total() or player.lost:
					print(f"{player.name} loses.")
				elif self.dealer.hand_total() == player.hand_total():
					print("Push.")
					player.chips += player.bet
				else:
					print(f"{player.name} wins!")
					player.chips += player.bet * 2
				print(f"{player.name} chips: {player.chips}")

	def clear_table(self):
		"""
		Resets hands and variables of players.

		Returns:
			None
		"""
		for player in self.player_list:
			player.reset_hand()
			player.lost = False
			player.blackjack = False
		self.dealer.reset_hand()

	@staticmethod
	def greeting_message():
		print()
		print("Hey there! Welcome to Blackjack.")
		print()

	@staticmethod
	def game_message(message):
		print()
		print("|-----------------------------------|")
		print(f"{message:^37}")
		print("|-----------------------------------|")
