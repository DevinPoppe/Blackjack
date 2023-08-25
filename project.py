import random
import os
import time
import sys
import argparse

parser = argparse.ArgumentParser(
    description="Play a game of Blackjack. You can define the amount of decks of cards for the game and the amount of rounds you want to play.",
    epilog="For example, a Blackjack game with 2 decks and 5 rounds:\npython Blackjack.py -p 2 5",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    "-r", "--rules", action="store_true", help="Show the rules of Blackjack."
)
parser.add_argument(
    "-p",
    "--play",
    type=int,
    nargs=2,
    metavar=("decks", "rounds"),
    help="Play a game of Blackjack. Define the amount of decks of cards for the game (1 - 10) and the amount of round you want to play (1 - 10).",
)


class Card:
    """
    A playing card with a symbol, number and value

    :param symbol (str): The suit of the card, e.g. Diamonds, Clubs.
    :param number (str): The number of the card, e.g. 6 or Queen.
    :param value (int): A dictionary mapping the corresponding numbers to their values.

    To create a card:
    card = Card("♣", "3", 3)

    """

    def __init__(self, symbol, number, value):
        self.symbol = symbol
        self.number = number
        self.value = value

    def __str__(self):
        return f"{self.number}:{self.symbol}:{self.value} Card"


def main(rounds_to_play=5, deck_amount=1):
    """
    Play Blackjack

    :param rounds_to_play (int): The number of rounds to play.
    :param deck_amount (int): The number of decks of cards to use.

    Displays a welcome message, then plays the Blackjack rounds and shows the final score after all rounds were played.

    """
    clear_screen()
    print(f"A game of Blackjack with {deck_amount} deck(s) and {rounds_to_play} round(s).")
    input("Press enter to continue.")

    wins = 0

    for round in range(rounds_to_play):
        clear_screen()

        # Creates players and dealers hand.
        player_cards = []
        players_cards_total_value = 0

        dealers_cards = []
        dealers_cards_total_value = 0

        # Hand cards to start with and check if both player cards are an Ace.
        player_cards.append(deal_card())
        player_cards.append(deal_card())

        for card in player_cards:
            if card.value == 11 and players_cards_total_value > 21:
                card.value = 1
                players_cards_total_value -= 10

        dealers_cards.append(deal_card())

        dealers_cards_total_value, players_cards_total_value = print_all(
            player_cards,
            players_cards_total_value,
            dealers_cards,
            dealers_cards_total_value,
        )

        # Checking for input as long as someone can make a move.
        while players_cards_total_value < 21 and dealers_cards_total_value < 21:
            action = input("Type S for Stand or H for Hit: ").upper()
            if action == "H" or action == "HIT":
                player_cards.append(deal_card())
                _, players_cards_total_value = print_all(
                    player_cards,
                    players_cards_total_value,
                    dealers_cards,
                    dealers_cards_total_value,
                )
                for card in player_cards:
                    if card.value == 11 and players_cards_total_value > 21:
                        card.value = 1
                        players_cards_total_value -= 10

                    _, players_cards_total_value = print_all(
                        player_cards,
                        players_cards_total_value,
                        dealers_cards,
                        dealers_cards_total_value,
                    )

            elif action == "S" or action == "STAND":
                while dealers_cards_total_value < 16:
                    dealers_cards.append(deal_card())

                    dealers_cards_total_value, _ = print_all(
                        player_cards,
                        players_cards_total_value,
                        dealers_cards,
                        dealers_cards_total_value,
                    )
                    for card in dealers_cards:
                        if card.value == 11 and dealers_cards_total_value > 21:
                            card.value = 1
                            dealers_cards_total_value -= 10

                        dealers_cards_total_value, _ = print_all(
                            player_cards,
                            players_cards_total_value,
                            dealers_cards,
                            dealers_cards_total_value,
                        )
                        break
                    time.sleep(0.85)
                break
        # Determinig the winner of current round and increasing the wins variable.
        if players_cards_total_value == 21:
            if len(player_cards) == 2:
                print("\nYou have a Blackjack!\nYou win!")
                wins += 1
            else:
                print("\nYou win with 21!")
                wins += 1
        elif players_cards_total_value > 21:
            print("\nYou bust, Dealer wins!")
        elif dealers_cards_total_value == 21:
            if len(dealers_cards) == 2:
                print("\nDealer wins with a Blackjack!")
            else:
                print("\nDealer wins with 21!")
        elif dealers_cards_total_value > 21:
            print("\nDealer busts, You win!")
            wins += 1
        elif 21 - dealers_cards_total_value < 21 - players_cards_total_value:
            print("\nDealer wins!")
        elif 21 - dealers_cards_total_value > 21 - players_cards_total_value:
            print("\nYou win!")
            wins += 1
        else:
            print("\nDraw!\n")

        if round == rounds_to_play - 1:
            input("Press enter to display the final score.")
        else:
            input(f"Press enter to advance to round {round + 2}/{rounds_to_play}.")

    clear_screen()
    print(f"You won {wins}/{rounds_to_play} rounds of Blackjack.")
    if wins == 0:
        message = "Better luck next time."
    elif wins == rounds_to_play:
        message = "Pure luck I guess!"
    elif wins == rounds_to_play / 2:
        message = "Not bad!"
    elif wins > rounds_to_play / 2:
        message = "Impressive."
    else:
        message = "Decent."
    print(message)
    print(f"\nThank you for playing.\n")


def print_all(
    player_cards,
    players_cards_total_value,
    dealers_cards,
    dealers_cards_total_value,
):
    """
    Display the current state of the game, showing both dealer's and player's cards.

    :param player_cards (list): List of Card objects representing the player's cards.
    :param players_cards_total_value (int): Total value of the player's cards.
    :param dealers_cards (list): List of Card objects representing the dealer's cards.
    :param dealers_cards_total_value (int): Total value of the dealer's cards.

    :return: The updated dealer's cards total value and player's cards total value.
    """
    clear_screen()
    print("\nDealers Cards:")
    dealers_cards_total_value = print_cards(dealers_cards)
    print(f"Total Value: {dealers_cards_total_value}\n\n")

    print("Your Cards:")
    players_cards_total_value = print_cards(player_cards)
    print(f"Total Value: {players_cards_total_value}\n")

    return dealers_cards_total_value, players_cards_total_value


def deal_card():
    """
    Draw a random card from the deck(s).
    Remove the card from the deck(s) so that it cannot be drawn again, only in the case when there are multiple decks.
    Return the drawn Card.
    """
    card = random.choice(deck)
    deck.remove(card)
    return card


def print_cards(current_hand):
    """
    Display the cards on the terminal.

    :param current_hand: List of Card objects representing the cards in a hand.

    Displays the cards in ones hand in a visually formatted style on the terminal.
    Each card is shown as a visual representation with suit symbol and card number.
    The cards a printed line by line next to each other with 5 spaces in between.
    If the card number is 10 the innner card is altered so it fits two decimals instead of one.
    The total value of the player's cards is calculated and returned.

    :return cards_total_value (int): Total value of Cards in ones hand.
    """
    display = ""

    for card in current_hand:
        display += "    ┌─────────┐ "
    print(display)
    display = ""

    for card in current_hand:
        if card.number == "10":
            display += "    │{}       │ ".format(card.number)
        else:
            display += "    │{}        │ ".format(card.number)
    print(display)
    display = ""

    print_empty_lines(len(current_hand))

    for card in current_hand:
        display += "    │    {}    │ ".format(card.symbol)
    print(display)
    display = ""

    print_empty_lines(len(current_hand))

    for card in current_hand:
        if card.number == "10":
            display += "    │    {}   │ ".format(card.number)
        else:
            display += "    │       {} │ ".format(card.number)
    print(display)
    display = ""

    for card in current_hand:
        display += "    └─────────┘ "
    print(display)
    display = ""

    print("\a", end="")

    cards_total_value = 0

    for card in current_hand:
        cards_total_value += card.value

    return cards_total_value


def print_empty_lines(n):
    """
    Create and print 2 empty card lines for the cards.

    :param n: The number of cards in the possession of the user or dealer.
    """
    display = ""
    for _ in range(2):
        for _ in range(n):
            display += "    │         │ "
        print(display)
        display = ""


def clear_screen():
    # Clear the terminal screen.
    os.system("cls")


def create_deck(numbers, symbols, value, decks=1):
    """
    Create a full deck of cards or multiple decks of cards.

    :param numbers: The number of the card, e.g. 6 or Queen.
    :param symbols: The suit of the card, e.g. Diamonds, Clubs.
    :param value: A dictionary mapping the corresponding numbers to their values.
    :param decks: The amount of decks the user wants to play with, default = 1.

    :return: A list containing Card objects representing the complete deck(s).
    """
    deck = []

    for _ in range(decks):
        for n in numbers:
            for s in symbols:
                deck.append(Card(s, n, value[n]))

    return deck


if __name__ == "__main__":
    """
    Blackjack Game Entry Point

    Command-line options:
    --rules     Displayes the rules
    --play      Starts a game of Blackjack

    When using --play, you can define the number of decks of cards and the number of rounds to play.
    Both arguments are set to their default values if they are out of bounds.
    Nessesary constants a generated and a game is started by the 'main()' function.

    Example usage:
    - To play 5 rounds of Blackjack with 2 decks: python Blackjack.py --play 2 5

    When no argparse argument is provided the help screen will be displayed.
    """

    args = parser.parse_args()

    if args.rules:
        clear_screen()
        print(
            "Rules of Blackjack:\n"
            " 1. The goal is to have a hand value closer to 21 than the dealer without going over.\n"
            " 2. You can 'Hit' to get more cards or 'Stand' to keep your current hand.\n"
            " 3. The dealer must hit if their hand value is less than 16.\n"
            " 4. If your hand value goes over 21, you bust and lose.\n"
            " 5. If both you and the dealer have the same value, it's a draw.\n"
            " 6. Blackjack is when you have an Ace and a 10-valued card.\n\n"
            "Hand Values:\n"
            " · Number cards are worth their face value.\n"
            " · Jacks, queens and king are worth 10.\n"
            " · Aces vary depending on the situation as either 1 or 11.\n\n"
            "type: 'python Blackjack -p 2 5' to play 5 rounds of Blackjack with 2 decks.\n"
        )
    elif args.play:
        deck_amount, rounds_to_play = args.play
        deck_amount = 10 if deck_amount > 10 else 1 if rounds_to_play < 1 else deck_amount
        rounds_to_play = 10 if rounds_to_play > 10 else 5 if rounds_to_play < 1 else rounds_to_play

        numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q", "A"]
        values = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 10,
            "K": 10,
            "Q": 10,
            "A": 11,
        }
        symbols = ["♣", "♦", "♥", "♠"]
        deck = create_deck(numbers, symbols, values)

        main(rounds_to_play, deck_amount)
    else:
        clear_screen()
        parser.print_help()
        sys.exit()
