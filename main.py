# -*- coding: utf-8 -*-
"""
Executes blackjack game.

Todo:
	* Create betting system
	* Create rule system
"""
from game_objects import Card, Deck, Player


def greeting_message():
	print()
	print("Hey there! Welcome to Blackjack.")
	print()


def take_bets(player_list):
	"""
	Takes bets for all players.

	Args:
		player_list (list): All active players.

	Returns:
		None
	"""
	for player in player_list:
		if not player.dealer:
			player.get_bet()
			print(f"Chips remaining: {player.chips}")


def deal_hands(player_list, deck):
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
			player.draw_card(deck)


def take_turns(player_list, dealer, deck):
	"""
	Takes turn for all players including dealer

	Args:
		player_list (list): All active players.
		dealer (object): dealer from player_list
		deck (object): From Deck class.

	Returns:
		None
	"""
	for player in player_list:
		if not player.dealer:
			turn_over = False
			loss = False
			while not turn_over:
				if player.hand_total() > 21:
					loss = True
					turn_over = True
				player.print_hand()
				dealer.print_hand()
				turn_over = player.get_move(deck)

	while dealer.hand_total() < 17:
		dealer.draw_card(deck)
		dealer.print_hand(show_dealer=True)
	print()
	print("|-----------------------------------|")
	print("               Results               ")
	print("|-----------------------------------|")
	if dealer.hand_total() > 21:
		print("\nBUST! House loses!\n")
		return
	for player in player_list:
		player.print_hand(show_dealer=True)
		if not player.dealer:
			print()
			if dealer.hand_total() > player.hand_total():
				print(f"{player.name} loses.")
			elif dealer.hand_total() == player.hand_total():
				print("Push.")
				player.chips += player.bet
			else:
				print(f"{player.name} wins!")
				player.chips += player.bet * 2
			print(f"{player.name} chips: {player.chips}")


def clear_table(player_list):
	"""
	Resets hands of players

	Args:
		player_list (list): All active players.

	Returns:
		None
	"""
	for player in player_list:
		player.reset_hand()


def play_game():
	"""
	Runs blackjack game until player exits.

	Returns:
		None
	"""
	player1 = Player(name="Frank")
	dealer = Player(dealer=True)
	player_list = [player1, dealer]
	deck = Deck(decks=1)

	playing = True
	greeting_message()
	while playing:
		take_bets(player_list)
		deal_hands(player_list, deck)
		take_turns(player_list, dealer, deck)
		clear_table(player_list)

		deck.shuffle_check(.70)
		print("\nNext round starting. . .")
		if input("\nPress 'x' to leave the table: ") == "x":
			playing = False


def main():
	play_game()


if __name__ == '__main__':
	main()
