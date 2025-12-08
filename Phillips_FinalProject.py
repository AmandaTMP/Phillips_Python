import random
import db

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

def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21

def get_bet(money):
    while True:
        try:
            bet = float(input("Bet amount: "))
        except ValueError:
            print("Bet must be a number.")
            continue

        if bet < MIN_BET:
            print(f"Minimum bet is {MIN_BET}.")
        elif bet > MAX_BET:
            print(f"Maximum bet is {MAX_BET}.")
        elif bet > money:
            print("Bet can't be greater than your current money.")
        else:
            return bet

def show_hand(label, hand):
    print(f"\n{label}")
    for card in hand:
        print(f"{card[0]} of {card[1]}")

def buy_chips(money):
    print(f"Money: {money:.2f}")
    choice = input("Your money is below the minimum bet. Buy more chips? (y/n): ")
    if choice.lower() == "y":
        while True:
            try:
                amount = float(input("Amount to add: "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                else:
                    money += amount
                    break
            except ValueError:
                print("Amount must be a valid number.")
    return money

def main():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2\n")

    money = db.read_money()

    while True:
        if money < MIN_BET:
            money = buy_chips(money)
            db.write_money(money)
            if money < MIN_BET:
                print("You still don't have enough to play. Bye!")
                break

        print(f"Money: {money:.2f}")
        bet = get_bet(money)

        deck = create_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]

        print("\nDEALER'S SHOW CARD:")
        show = dealer_hand[0]
        print(f"{show[0]} of {show[1]}")

        show_hand("YOUR CARDS:", player_hand)

        player_blackjack = is_blackjack(player_hand)
        dealer_blackjack = is_blackjack(dealer_hand)

        if not player_blackjack and not dealer_blackjack:
            while True:
                choice = input("\nHit or stand? (hit/stand): ")
                if choice.lower() == "hit":
                    player_hand.append(deck.pop())
                    show_hand("YOUR CARDS:", player_hand)
                    if hand_value(player_hand) > 21:
                        break
                elif choice.lower() == "stand":
                    break
                else:
                    print("Please enter 'hit' or 'stand'.")

        player_points = hand_value(player_hand)
        dealer_points = hand_value(dealer_hand)

        if player_points <= 21 and not dealer_blackjack:
            while dealer_points < 17:
                dealer_hand.append(deck.pop())
                dealer_points = hand_value(dealer_hand)

        show_hand("DEALER'S CARDS:", dealer_hand)
        print(f"\nYOUR POINTS: {player_points}")
        print(f"DEALER'S POINTS: {dealer_points}")

        if player_blackjack and not dealer_blackjack:
            win_amount = round(bet * 1.5, 2)
            print(f"Blackjack! You win {win_amount:.2f}.")
            money += win_amount
        elif dealer_blackjack and not player_blackjack:
            print("Dealer has blackjack. You lose.")
            money -= bet
        elif player_points > 21:
            print("You bust. You lose.")
            money -= bet
        elif dealer_points > 21:
            print("Dealer busts. You win!")
            money += bet
        elif player_points > dealer_points:
            print("You win!")
            money += bet
        elif player_points < dealer_points:
            print("Dealer wins.")
            money -= bet
        else:
            print("Push.")

        db.write_money(money)
        print(f"Money: {money:.2f}\n")

        again = input("Play again? (y/n): ")
        if again.lower() != "y":
            print("Come back soon!")
            break

    print("Bye!")

if __name__ == "__main__":
    main()