import random

def main():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    print()

    money = 100.0
    print(f"Money: {money}")

    while True:
        bet = float(input("Bet amount: "))
        
        player_points = random.randint(1, 30)
        dealer_points = random.randint(1, 30)

        print(f"\nYOUR POINTS: {player_points}")
        print(f"DEALER'S POINTS: {dealer_points}")

        if player_points > 21:
            print("You bust. You lose.")
            money -= bet
        elif dealer_points > 21 or player_points > dealer_points:
            print("You win!")
            money += bet
        elif player_points == dealer_points:
            print("Tie.")
        else:
            print("Dealer wins.")
            money -= bet

        print(f"Money: {money}")
        print()

        again = input("Play again? (y/n): ")
        if again != "y":
            break

    print("Bye!")

if __name__ == "__main__":
    main()
