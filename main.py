"""ADS Final Project
A black-jack implementation in Python.
Using:
+ Pygame
"""
import pygame
import random
import sys
import time
from typing import List, Tuple



def CalculateHandValue(hand : list) -> int: # O(n) - no loops just recursion over the list
    """Calculate the value of the hand.
    Args:
        hand (list): list of cards [where a card is a tuple of (suit, value)]
    Returns:
        int: value of the hand
    Process:
    Number cards have a value equal to their number, while all the picture cards (Jacks, Queens, and Kings) are worth 10. Aces can be worth 11 or one, whichever is more beneficial to the person holding the hand. For example, a hand with an Ace and an Eight is worth 19 (the Ace is valued at 11, known as a soft Ace). A hand with an Ace, a Four, and a Nine is worth 14 (the Ace is valued at one, known as a hard Ace, because if it were valued at 11 the hand would bust).
    https://entertainment.howstuffworks.com/blackjack2.htm
    """
    legend = {
        'A': lambda x: 11 if x + 11 <= 21 else 1, # we need to see if we should use a soft ace or a hard ace
        # gotta love lambda functions :)
        'J': 10,
        'Q': 10,
        'K': 10,
        }
    if hand == []:
        return 0
    if hand[0][0] in legend:
        handFilter = legend[hand[0][0]]
        if callable(handFilter): # check callable for A
            # pylint: disable=line-too-long
            return handFilter(CalculateHandValue(hand[1:])) + CalculateHandValue(hand[1:])
        else:
            return handFilter + CalculateHandValue(hand[1:])
    else:
        return hand[0][0] + CalculateHandValue(hand[1:])

def ShuffleDeck(deck: list) -> list: # O(n)
    """Shuffle the deck.
    Args:
        deck (list): list of cards
    Returns:
        list: shuffled deck
    """
    # this algorithm is called Fisher-Yates shuffle
    # https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle

    n = len(deck)
    while n > 1: # O(n)
        n -= 1
        k = random.randint(0, n) # we take some random item j
        deck[k], deck[n] = deck[n], deck[k] # we just swap the last index with the random index
        # where the last index moves closer to the beginning of the list
    return deck

def DealCard(deck: list) -> Tuple[str, int]: # O(1)
    """Deal a card from the deck.
    Args:
        deck (list): list of cards
    Returns:
        tuple: card
    """
    return deck.pop()

def DealHand(deck: list) -> List[Tuple[str, int]]: # O(1)
    """Deal a hand from the deck.
    Args:
        deck (list): list of cards
    Returns:
        list: hand
    """
    return [DealCard(deck) for _ in range(2)]

def PrettyPrintCard(card: Tuple[str, int]) -> str: # O(1)
    """Pretty print a card.
    Args:
        card (tuple): card
    Returns:
        str: pretty printed card
    """
    # S = S, ♥ = H, ♦ = D, ♣ = C
    symbol = {
        'S': '♠',
        'H': '♥',
        'D': '♦',
        'C': '♣',
        }
    # TODO Make a verbose function that gives use the full name of the card
    print(f'{symbol[card[1]]} {card[0]}')

def main():
    pygame.init()
    pygame.display.set_caption('Black Jack')
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()
        clock.tick(60)

def winner(playerHand: list, dealerHand: list) -> str:
    """Select the winner.
    Args:
        playerHand (list): player's hand
        dealerHand (list): dealer's hand

    Returns:
        str: winner

    1. If the player's hand is greater than 21, the player busts and automatically loses.
    2. If the dealer's hand is greater than 21, the dealer busts and automatically loses.
    3. If the player's hand is greater than the dealer's hand, the player wins.
    4. If the dealer's hand is greater than the player's hand, the dealer wins.
    5. If the player's hand is equal to the dealer's hand, it is a tie.
    """
    playerValue = CalculateHandValue(playerHand)
    dealerValue = CalculateHandValue(dealerHand)

    if playerValue > 21:
        return 'Dealer'
    elif dealerValue > 21:
        return 'Player'
    elif playerValue > dealerValue:
        return 'Player'
    elif dealerValue > playerValue:
        return 'Dealer'
    else:
        return 'Tie'

def DealerAI(dealerHand: list) -> bool:
    """A Simple algorithm to determine if the dealer should hit or stand.
    Args:
        dealerHand (list): dealer's hand
    Returns:
        bool: True = hit, False = stand
    1. If the dealer's hand is less than 17, the dealer must hit.
    2. If the dealer's hand is greater than or equal to 17, the dealer must stand.
    """
    if CalculateHandValue(dealerHand) < 17:
        return True
    else:
        return False

def main_cli():
    """
    1. The dealer gives each player two cards including himself.
    2. The dealer has one card face up and one card face down.
    3. The player can choose to hit or stand.
    4. If the player hits, he gets another card.
    5. If the player stands, the dealer will reveal his face down card.
    6. We call another function to determine the winner.
    """
    deck = ShuffleDeck([(value, suit) for suit in ['S', 'H', 'D', 'C'] for value in range(2, 11)] + [(value, suit) for suit in ['S', 'H', 'D', 'C'] for value in ['J', 'Q', 'K', 'A']])

    playerHand = DealHand(deck)
    dealerHand = DealHand(deck)

    # this is all from the perspective of the player
    print('Your hand is:')
    for card in playerHand:
        PrettyPrintCard(card)
    print('Value of your hand:', CalculateHandValue(playerHand))

    print('The dealer\'s hand is:')
    PrettyPrintCard(dealerHand[0])
    print('The dealer\'s second card is face down.')

    while True:
        print('Do you want to hit or stand?')
        print('1. Hit')
        print('2. Stand')
        choice = input('Enter your choice: ')

        if choice == '1':
            playerHand.append(DealCard(deck))
            print('Your hand is:')
            for card in playerHand:
                PrettyPrintCard(card)
            print('Value of your hand:', CalculateHandValue(playerHand))
            if CalculateHandValue(playerHand) > 21:
                print('You busted!')
                break
        elif choice == '2':
            # let the dealer play
            while DealerAI(dealerHand):
                dealerHand.append(DealCard(deck))
            print('The dealer\'s hand is:')
            for card in dealerHand:
                PrettyPrintCard(card)
            print('Value of the dealer\'s hand:', CalculateHandValue(dealerHand))
            break

        if CalculateHandValue(playerHand) == 21:
            print('You got a blackjack!')
            break



main_cli()
