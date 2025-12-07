import random

MONEY_FILE = "money.txt"
MIN_BET = 5
MAX_BET = 1000

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
    total = sum(card[2] for card in hand)
    aces = sum(1 for card in hand if card[0] == "Ace")

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def read_money():
    try:
        with open(MONEY_FILE, "r") as file:
            text = file.read().strip()
            if text == '':
                return 100.0
            return float(text)
    except (FileNotFoundError, ValueError):
        return 100.0
    
def write_money(money):
    with open(MONEY_FILE, "w") as file:
        file.write(str(round(money, 2)))

def get_bet(money):
    while True:
        try:
            bet = float(input("Bet amount:  "))
        except ValueError:
            print("Bet must be a number.")
            continue 

        if bet < MIN_BET:
            print(f"Minimum bet is {MIN_BET}.")
        elif bet > MAX_BET:
            print(f"Maximum bet is {MAX_BET}.")
        elif bet > money:
            print("Bet can't be greater than current money.")
        else:
            return bet 
        
def show_hand(label, hand, hide_first = False):
    print(f"\n{label}")
    for i, card in enumerate(hand):
        if hide_first and i == 1:
            continue
        print(f"{card[0]} of {card[1]}")

def main():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2\n")

    money = read_money()

    while True:
        print(f"Money: {money}")
        bet = get_bet(money)

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
                show_hand("YOUR CARDS:", player_hand)
                if hand_value(player_hand) > 21:
                    break
            elif choice == "stand":
                break
            else:
                print("Please enter 'hit' or 'stand'.")

        player_points = hand_value(player_hand)
        dealer_points = hand_value(dealer_hand)

        if player_points <= 21:
            while dealer_points < 17:
                dealer_hand.append(deck.pop())
                dealer_points = hand_value(dealer_hand)

        print("\nDEALER'S CARDS:", dealer_hand)
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