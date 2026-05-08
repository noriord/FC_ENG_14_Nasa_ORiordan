from ast import literal_eval
import os

# --- File Configuration ---
DATA_FILE = "company_data.txt"


def load_data():
    """Load saved state from file - one item per line."""
    if not os.path.exists(DATA_FILE):
        print("No saved data found. Starting fresh.")
        return 0.0, {}, {}, []

    try:
        with open(DATA_FILE, "r") as fd:
            balance = literal_eval(fd.readline().strip())
            products = literal_eval(fd.readline().strip())
            sales = literal_eval(fd.readline().strip())
            operations = literal_eval(fd.readline().strip())
        print("Data loaded successfully.")
        return balance, products, sales, operations
    except (SyntaxError, ValueError, IOError) as e:
        print("Warning: Could not load data file ({}). Starting fresh.".format(e))
        return 0.0, {}, {}, []


def save_data(account_balance, products, sales, operations):
    """Save current state to file - one item per line."""
    try:
        with open(DATA_FILE, "w") as fd:
            fd.write(repr(account_balance) + "\n")
            fd.write(repr(products) + "\n")
            fd.write(repr(sales) + "\n")
            fd.write(repr(operations) + "\n")
        print("Data saved successfully.")
    except IOError as e:
        print("Error: Could not save data ({}).".format(e))



# --- Load data from file at startup ---
account_balance, products, sales, operations = load_data()

# --- Main Program Loop ---
while True:
    print()
    print("0.end")
    print("1.balance")
    print("2.sale")
    print("3.purchase")
    print("4.account")
    print("5.list")
    print("6.warehouse")
    print("7.review")

    try:
        choice = int(input("Choose option: "))
    except ValueError:
        print("Wrong option")
        continue

    if choice == 0:
        save_data(account_balance, products, sales, operations)
        print("Thank you! Bye :)")
        break

    elif choice == 1:
        print("balance")
        try:
            amount = float(input("Enter amount to add or subtract (negative, positive): "))
        except ValueError:
            print("Invalid amount.")
            continue
        operations.append(("balance", amount))
        account_balance = account_balance + amount
        print("Balance updated: {}".format(account_balance))

    elif choice == 2:
        print("sale")
        product = input("Enter product name: ")
        if not product:
            print("Product name cannot be empty.")
            continue

        try:
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price per unit: "))
        except ValueError:
            print("Invalid quantity or price.")
            continue

        if quantity <= 0:
            print("Quantity must be a positive number.")
            continue

        if price < 0:
            print("Price cannot be negative.")
            continue

        if product not in products:
            print("'{}' is not in the warehouse.".format(product))
            continue

        if products[product]["quantity"] < quantity:
            print("Not enough stock. Available: {}".format(products[product]["quantity"]))
            continue

        revenue = price * quantity
        account_balance = account_balance + revenue
        products[product]["quantity"] = products[product]["quantity"] - quantity

        if product in sales:
            sales[product] = sales[product] + quantity
        else:
            sales[product] = quantity

        if products[product]["quantity"] == 0:
            del products[product]

        operations.append(("sale", product, price, quantity))
        print("Sold {} x '{}'. Revenue: {}".format(quantity, product, revenue))
        print("Current balance: {}".format(account_balance))

    elif choice == 3:
        print("purchase")
        product = input("Enter product name: ")
        if not product:
            print("Product name cannot be empty.")
            continue

        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid quantity.")
            continue

        if quantity <= 0:
            print("Quantity must be a positive number.")
            continue

        try:
            price = float(input("Enter price per unit: "))
        except ValueError:
            print("Invalid price.")
            continue

        if price < 0:
            print("Price cannot be negative.")
            continue

        cost = price * quantity

        if account_balance - cost < 0:
            print("Not enough funds! Balance: {}, Cost: {}".format(account_balance, cost))
            continue

        account_balance = account_balance - cost

        if product in products:
            products[product]["quantity"] = products[product]["quantity"] + quantity
            products[product]["price"] = price
        else:
            products[product] = {"price": price, "quantity": quantity}

        operations.append(("purchase", product, price, quantity))
        print("Purchased {} x '{}'. Cost: {}".format(quantity, product, cost))
        print("Current balance: {}".format(account_balance))

    elif choice == 4:
        print("account")
        print("Current balance: {}".format(account_balance))

    elif choice == 5:
        print("list")
        if not products:
            print("Warehouse is empty.")
        else:
            for product, info in products.items():
                print("{} - Price: {}, Quantity: {}".format(product, info["price"], info["quantity"]))

        if sales:
            print("Total products sold:")
            for product, qty in sales.items():
                print("  {}: {} units".format(product, qty))

    elif choice == 6:
        print("warehouse")
        product = input("Enter product name: ")

        if product in products:
            print("{} - Price: {}, Quantity: {}".format(
                product, products[product]["price"], products[product]["quantity"]))
        else:
            print("'{}' is not in the warehouse.".format(product))

    elif choice == 7:
        print("review")
        if not operations:
            print("No operations recorded yet.")
            continue

        from_text = input("From index (press Enter for start): ")
        to_text = input("To index (press Enter for end): ")

        if from_text == "":
            from_idx = 0
        else:
            try:
                from_idx = int(from_text)
            except ValueError:
                print("Invalid index.")
                continue

        if to_text == "":
            to_idx = len(operations)
        else:
            try:
                to_idx = int(to_text)
            except ValueError:
                print("Invalid index.")
                continue

        if from_idx < 0:
            from_idx = 0
        if to_idx > len(operations):
            to_idx = len(operations)
        if from_idx >= to_idx:
            print("Invalid range.")
            continue

        for i in range(from_idx, to_idx):
            op = operations[i]
            if op[0] == "balance":
                print("[{}] Balance: {}".format(i, op[1]))
            elif op[0] == "sale":
                print("[{}] Sale: {} x '{}' at {}".format(i, op[3], op[1], op[2]))
            elif op[0] == "purchase":
                print("[{}] Purchase: {} x '{}' at {}".format(i, op[3], op[1], op[2]))

    else:
        print("Wrong option")
