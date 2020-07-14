# -*- coding: utf-8 -*-
"""
Executes blackjack game.

Todo:
	* Create turn system
	* Create betting system
	* Create rule system
"""
from game_objects import Card, Deck, Player


def greeting_message():
	print()
	print("Hey there! Welcome to Blackjack.")
	print()


def get_bet(player):
	"""
	Get user input, only accepts integers. Checks remaining chips

	Args:
		player (object): Created from Player class.
	Returns:
		int : Valid bet.
	"""
	while True:
		try:
			print()
			print(f"You have {player.chips} chips.")
			userInput = int(input("Place your bet: "))
		except ValueError:
			print("Must be a whole number! Try again.")
			continue
		else:
			if userInput > player.chips:
				print(f"Not enough chips remaining. Try again.")
				continue
			elif userInput <= 0:
				print(f"Invalid bet. Try again.")
				continue
			else:
				return userInput
				break


def deal_hand(player_list, deck):
	"""
	Deals hand to all players.

	Args:
		player_list (list): All active players.
		deck (object): From Deck class.

	Returns:
		None

	"""
	for card_num in range(1, 3):
		for player in player_list:
			card = deck.deal_card()
			player.hand.append(card)


def play_game():
	"""
	Runs blackjack game until player exits.

	Returns:
		None
	"""

	player1 = Player(name="Frank")
	dealer = Player(dealer=True)
	player_list = [player1, dealer]
	deck = Deck(decks=4)

	playing = True
	greeting_message()
	while playing:
		bet = get_bet(player1)
		player1.chips -= bet
		print(f"Chips remaining: {player1.chips}")
		deal_hand(player_list, deck)
		for player in player_list:
			player.print_hand()

		if input("\nPress 'x' to leave the table: ") == "x":
			playing = False


def main():
	play_game()


if __name__ == '__main__':
	main()
