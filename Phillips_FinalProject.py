import random

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = [
    ("Ace", 11),
    ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6),
    ("7", 7), ("8", 8), ("9", 9), ("10", 10),
    ("Jack", 10), ("Queen", 10), ("King", 10)
]

def create_deck():
    deck = []
    for suit in SUITS:
        for rank, value in RANKS:
            deck.append([rank, suit, value])
    random.shuffle(deck)
    return deck

def hand_value(hand):
    total = 0
    for card in hand:
        total += card[2]
    return total

def main():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2\n")

    money = 100.0

    while True:
        print(f"Money: {money}")
        bet = float(input("Bet amount: "))

        deck = create_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]

        print("\nDEALER'S SHOW CARD:")
        show = dealer_hand[0]
        print(f"{show[0]} of {show[1]}")

        print("\nYOUR CARDS:")
        for card in player_hand:
            print(f"{card[0]} of {card[1]}")

        while True:
            choice = input("\nHit or stand? (hit/stand): ")
            if choice == "hit":
                player_hand.append(deck.pop())
                print("\nYOUR CARDS:")
                for card in player_hand:
                    print(f"{card[0]} of {card[1]}")
                if hand_value(player_hand) > 21:
                    break
            else:
                break

        player_points = hand_value(player_hand)
        dealer_points = hand_value(dealer_hand)

        if player_points <= 21:
            while dealer_points < 17:
                dealer_hand.append(deck.pop())
                dealer_points = hand_value(dealer_hand)

        print("\nDEALER'S CARDS:")
        for card in dealer_hand:
            print(f"{card[0]} of {card[1]}")
        print(f"\nYOUR POINTS: {player_points}")
        print(f"DEALER'S POINTS: {dealer_points}")

        if player_points > 21:
            print("Sorry. You lose.")
            money -= bet
        elif dealer_points > 21 or player_points > dealer_points:
            print("You win!")
            money += bet
        elif player_points == dealer_points:
            print("Push.")
        else:
            print("Dealer wins.")
            money -= bet

        print(f"Money: {money}\n")

        again = input("Play again? (y/n): ")
        if again != "y":
            break

    print("Bye!")

if __name__ == "__main__":
    main()