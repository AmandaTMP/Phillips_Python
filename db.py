MONEY_FILE = "money.txt"

def read_money():
    try:
        with open(MONEY_FILE, "r") as file:
            return float(file.read().strip())
    except FileNotFoundError:
        return 100.0
    
def write_money(money):
    with open(MONEY_FILE, "w") as file:
        file.write(f"{money: .2f}")