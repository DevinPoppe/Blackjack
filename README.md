# Blackjack Game

#### Video Demo: https://www.youtube.com/watch?v=JaEBTQDBLm4

## Description
This is a command-line implementation of the classic Blackjack card game. You play against the dealer.

## Features

- Play Blackjack with customizable options for the number of decks and rounds
- Follows the standard Blackjack game rules for gameplay
- Displays a visual representation of cards in the terminal

## Installation

1. Clone this repository to your local machine
2. Navigate to the repository and open a terminal window in the repository directory

## Usage/Example
### Display the rules
To view the rules of Blackjack, run the following command in your terminal:

```bash
python project.py --rules
```

### Play Blackjack
To play a game of Blackjack, run the following command in your terminal:

```bash
python project.py --play [decks] [rounds]
```

Replace '[decks]' with the number of decks you want to shuffle together (1-10) and '[rounds]' with the number of rounds you want to play (1-10). For instance:

```bash
python project.py --play 3 5
```
## Gameplay
 - Follow the prompt in the terminal to make decisions.
 - Type 'H' or 'Hit' to draw an additional card.
 - Type 'S' or 'Stand' to keep your current hand.
 - The dealer will automatically draw cards as long as their hand value is less than 16.
 - The game will determine whether you win, lose, or tie each round.
 - After all rounds are completed a final score will be displayed.

## About Me
Hello, I am Devin from Berlin, Germany, and this is my final project for CS50P. Last year I graduated high school and this year I will be starting my biology technician  apprenticeship.

 ---
 Please feel free to reach out if you have any questions or feedback.
 I hope you enjoy playing Blackjack.