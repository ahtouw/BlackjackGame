"""
Module for creating blackjack game.
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

		Args:
			player_list (list): All active players.
			deck (object): From Deck class.
		"""
		self.player_list = [Player(name="Frank")]
		self.dealer = Player(dealer=True)
		self.deck = Deck(decks=1)

	def run(self):
		"""
		Runs blackjack game until player exits.

		Returns:
			None
		"""
		playing = True
		self.greeting_message()
		while playing:
			self.take_bets()
			self.deal_hands()
			self.take_turns()
			self.clear_table()

			self.deck.shuffle_check(.70)
			print("\nNext round starting. . .")
			if input("\nPress 'x' to leave the table: ") == "x":
				playing = False

	@staticmethod
	def greeting_message():
		print()
		print("Hey there! Welcome to Blackjack.")
		print()

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
			loss = False
			while not turn_over:
				if player.hand_total() > 21:
					loss = True
					turn_over = True
				player.print_hand()
				self.dealer.print_hand()
				turn_over = player.get_move(self.deck)

		while self.dealer.hand_total() < 17:
			self.dealer.draw_card(self.deck)
			self.dealer.print_hand(show_dealer=True)
		print()
		print("|-----------------------------------|")
		print("               Results               ")
		print("|-----------------------------------|")

		self.dealer.print_hand(show_dealer=True)
		if self.dealer.hand_total() > 21:
			print("\nBUST! House loses!\n")
			return
		for player in self.player_list:
			player.print_hand()
			print()
			if self.dealer.hand_total() > player.hand_total():
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
		Resets hands of players

		Returns:
			None
		"""
		for player in self.player_list:
			player.reset_hand()
		self.dealer.reset_hand()
