from typing import Union
import random
import os
import time
def clear(): return os.system('clear')

# TODO handle betting


original_deck = (
    ('D', 2),
    ('D', 3),
    ('D', 4),
    ('D', 5),
    ('D', 6),
    ('D', 7),
    ('D', 8),
    ('D', 9),
    ('D', 10),
    ('D', 11),
    ('D', 12),
    ('D', 13),
    ('D', 14),
    ('C', 2),
    ('C', 3),
    ('C', 4),
    ('C', 5),
    ('C', 6),
    ('C', 7),
    ('C', 8),
    ('C', 9),
    ('C', 10),
    ('C', 11),
    ('C', 12),
    ('C', 13),
    ('C', 14),
    ('S', 2),
    ('S', 3),
    ('S', 4),
    ('S', 5),
    ('S', 6),
    ('S', 7),
    ('S', 8),
    ('S', 9),
    ('S', 10),
    ('S', 11),
    ('S', 12),
    ('S', 13),
    ('S', 14),
    ('H', 2),
    ('H', 3),
    ('H', 4),
    ('H', 5),
    ('H', 6),
    ('H', 7),
    ('H', 8),
    ('H', 9),
    ('H', 10),
    ('H', 11),
    ('H', 12),
    ('H', 13),
    ('H', 14),
)


def display_card_info(card: tuple) -> str:
    suite = ''
    value = card[1]
    if card[0] == 'S':
        suite = 'Spade'
    if card[0] == 'D':
        suite = 'Diamond'
    if card[0] == 'C':
        suite = 'Club'
    if card[0] == 'H':
        suite = 'Heart'
    if card[1] == 11:
        value = 'Jack'
    if card[1] == 12:
        value = 'Queen'
    if card[1] == 13:
        value = 'King'
    if card[1] == 14:
        value = 'Ace'

    return f"{value} of {suite}s"


def shuffle_deck(og_deck: tuple) -> list:
    possible_indicies = [i for i in range(len(og_deck))]
    new_deck = []
    while len(possible_indicies) > 0:
        random_card_ind = random.randrange(0, len(possible_indicies))
        card_ind = possible_indicies[random_card_ind]
        new_deck.append(original_deck[card_ind])
        possible_indicies.remove(card_ind)
    return new_deck


def main_menu(dealers_cards: list, players_cards: list, shuffled_deck: list) -> Union[int, None]:
    player_count = count_player_cards(players_cards)
    while True:
        dealer_face = dealers_cards[0]
        print(f"The dealer is showing a {display_card_info(dealer_face)}")
        print("You have: ")
        for card in players_cards:
            print(display_card_info(card))
        true_player_count = player_count[0]
        print(
            f"Your hand total is: {'Soft' if player_count[1] == True else ''} {true_player_count}")
        print("1. Stay")
        print("2. Hit")
        print("3. Quit")
        user_input = input("What would you like to do?\n")
        if user_input.isnumeric():
            if int(user_input) == 1:
                clear()
                dealer_count = play_dealers_hand(dealers_cards, shuffled_deck)
                compare_hands(dealer_count, player_count)
                time.sleep(3)
                return 1
            if int(user_input) == 2:
                clear()
                player_hit = hit(players_cards, shuffled_deck)
                print(f"You drew a {player_hit}")
                player_count = count_player_cards(players_cards)
                if player_count[0] > 21 and player_count[1] is False:
                    print("You Busted!")
                    time.sleep(2)
                    return 1
            if int(user_input) == 3:
                return None
        else:
            print("Invalid input")


def count_player_cards(player_cards: list) -> list:
    sum = 0
    is_soft = False
    amount_of_aces = 0
    for card in player_cards:
        card_value = card[1]
        if card_value <= 10:
            sum += card[1]
        elif card_value >= 11 and card_value < 14:
            sum += 10
        else:
            amount_of_aces += 1
            if sum <= 10:
                is_soft = True
                sum += 11
            else:
                sum += 1

        if sum > 21 and is_soft is True:
            sum -= 10
            is_soft = False
    return [sum, is_soft]


def hit(players_cards: list, shuffled_deck: list) -> str:
    card_drew = shuffled_deck.pop()
    players_cards.append(card_drew)
    return display_card_info(card_drew)


def play_dealers_hand(dealers_cards: list, shuffled_cards: list) -> tuple:
    dealer_total = count_player_cards(dealers_cards)
    is_dealer_hand_soft = dealer_total[1]
    print(f"The Dealer flipped a {display_card_info(dealers_cards[1])}")
    print(f"dealer total is: {dealer_total[0]}")
    # dealer stops at soft 17
    if is_dealer_hand_soft is True and dealer_total[0] >= 17 and dealer_total[0] <= 21:
        return dealer_total
    time.sleep(2)
    true_dealer_total = dealer_total[0]
    while true_dealer_total <= 16:
        dealer_hit = hit(dealers_cards, shuffled_cards)
        dealer_total = count_player_cards(dealers_cards)
        true_dealer_total = dealer_total[0]
        is_dealer_hand_soft = dealer_total[1]
        if is_dealer_hand_soft is True and true_dealer_total > 21:
            true_dealer_total -= 10
        if is_dealer_hand_soft is True and true_dealer_total >= 17 and true_dealer_total <= 21:
            return dealer_total
        print(f"The dealer drew a {dealer_hit}")
    return dealer_total


def compare_hands(dealers_count: int, players_count: int) -> None:
    if dealers_count[0] > 21 and dealers_count[1] is False:
        print(f"dealer busted with {dealers_count[0]}")
        print("you win")
        return
    if dealers_count[0] > 21 and dealers_count[1] is True and dealers_count[0] - 10 > 21:
        print(f"dealer busted with {dealers_count[0]}")
        print("you win!")
        return
    else:
        if dealers_count[1] is True and dealers_count[0] > 21:
            dealers_count[0] -= 10
        if players_count[1] is True and players_count[0] > 21:
            players_count[0] -= 10

        if dealers_count[0] < players_count[0]:
            print(
                f"You win with {players_count[0]} against dealers: {dealers_count[0]}")
        elif dealers_count[0] > players_count[0]:
            print(
                f"You lose with {players_count[0]} against dealers: {dealers_count[0]}")
        elif dealers_count[0] == players_count[0]:
            print(
                f"You push with {players_count[0]} against dealers: {dealers_count[0]}")


# setup the inital game
shuffled_deck = shuffle_deck(original_deck)

dealers_cards = []
dealers_cards.append(shuffled_deck.pop())
dealers_cards.append(shuffled_deck.pop())

players_cards = []
players_cards.append(shuffled_deck.pop())
players_cards.append(shuffled_deck.pop())


def reset_game():
    shuffled_deck = shuffle_deck(original_deck)

    dealers_cards = []
    dealers_cards.append(shuffled_deck.pop())
    dealers_cards.append(shuffled_deck.pop())
    players_cards = []
    players_cards.append(shuffled_deck.pop())
    players_cards.append(shuffled_deck.pop())

    print(f"this is the dealers cards {dealers_cards}")


while True:
    game = main_menu(dealers_cards, players_cards, shuffled_deck)
    if game == 1:
        clear()
        print("shuffling...")
        time.sleep(2)
        clear()

    shuffled_deck = shuffle_deck(original_deck)

    dealers_cards = []
    dealers_cards.append(shuffled_deck.pop())
    dealers_cards.append(shuffled_deck.pop())
    players_cards = []
    players_cards.append(shuffled_deck.pop())
    players_cards.append(shuffled_deck.pop())

    if game == None:
        break


# main_menu(dealers_cards[0], players_cards)
