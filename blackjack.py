# -*- coding: utf-8 -*-
"""
Module for creating blackjack game.

Todo:
	* Add double, split functions
"""
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
		"""
		self.player_list = [Player(name="Frank"), Player(name="Jane")]
		self.dealer = Player(dealer=True)
		self.deck = Deck(decks=4)

	def run(self):
		"""
		Runs blackjack game until player exits.

		Returns:
			None
		"""
		playing = True
		self.game_message("Welcome to Blackjack!")
		while playing:
			self.game_message("Place your bets")
			self.take_bets()
			self.deal_hands()
			self.take_turns()
			self.get_results()
			self.clear_table()

			self.deck.shuffle_check(.70)
			self.game_message("Continue?")
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
			self.game_message(f"{player.name}'s turn")
			player.print_hand()
			while not turn_over:
				self.dealer.print_hand(show_dealer=False)
				if player.has_blackjack():
					break
				turn_over = player.get_move(self.deck)
				player.print_hand()

		self.game_message(f"{self.dealer.name}'s turn")
		while self.dealer.score < 17:
			self.dealer.print_hand(show_dealer=True)
			print("Draw card.")
			self.dealer.draw_card(self.deck)
		self.dealer.print_hand(show_dealer=True)

	def get_results(self):
		"""
		Evaluates if player or dealer won hand.

		Returns:
			None
		"""
		self.game_message("Results")
		self.dealer.print_hand(show_dealer=True)
		for player in self.player_list:
			player.print_hand()
			print()
			if player.has_blackjack() and self.dealer.score != 21:
				print("---- BLACKJACK WINNER!!! ----")
				player.award_chips("blackjack")
			elif player.score > 21:
				print(f"Player bust, {player.name} loses.")
			elif self.dealer.score > 21:
				print("HOUSE BUST! House loses!")
				print(f"{player.name} wins!")
				player.award_chips("win")
			else:
				if self.dealer.score > player.score:
					print(f"{player.name} loses.")
				elif self.dealer.score == player.score:
					print("Push.")
					player.award_chips("push")
				else:
					print(f"{player.name} wins!")
					player.award_chips("win")
			print(f"{player.name}'s chips: {player.chips}")

	def clear_table(self):
		"""
		Resets hands and variables of players.

		Returns:
			None
		"""
		for player in self.player_list:
			player.reset_hand()
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
