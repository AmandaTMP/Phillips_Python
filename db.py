MONEY_FILE = "money.txt"

def read_money():
    try:
        with open(MONEY_FILE, "r") as file:
            text = file.read().strip()
            return float(text)
    except (FileNotFoundError, ValueError):
        return 100.0
    
def write_money(money):
    with open(MONEY_FILE, "w") as file:
        file.write(f"{money: .2f}")