
# ============================================================
# Company Account & Warehouse Simulator
# Using Manager class with decorators
# With LOAD and SAVE system
# ============================================================

import os


class Manager:
    """Manager class that handles accounting operations using decorators."""

    def __init__(self):
        self.actions = {}
        self.account_balance = 0.0
        self.products = {}
        self.sales = {}
        self.operations = []

    def assign(self, name):
        """Decorator that registers a function as an action."""
        def decorate(cb):
            self.actions[name] = cb
            return cb
        return decorate

    def execute(self, name):
        """Execute a registered action by name."""
        if name not in self.actions:
            print("Action '{}' is not defined.".format(name))
        else:
            self.actions[name](self)

    def save_to_file(self, filepath):
        """Save all data to a text file so it can be loaded later."""
        file = open(filepath, "w")

        # Save balance
        file.write("BALANCE\n")
        file.write("{}\n".format(self.account_balance))

        # Save products
        file.write("PRODUCTS\n")
        for product, info in self.products.items():
            file.write("{}|{}|{}\n".format(product, info["price"], info["quantity"]))
        file.write("END_PRODUCTS\n")

        # Save sales
        file.write("SALES\n")
        for product, qty in self.sales.items():
            file.write("{}|{}\n".format(product, qty))
        file.write("END_SALES\n")

        # Save operations
        file.write("OPERATIONS\n")
        for op in self.operations:
            if op[0] == "balance":
                file.write("balance|{}\n".format(op[1]))
            elif op[0] == "sale":
                file.write("sale|{}|{}|{}\n".format(op[1], op[2], op[3]))
            elif op[0] == "purchase":
                file.write("purchase|{}|{}|{}\n".format(op[1], op[2], op[3]))
        file.write("END_OPERATIONS\n")

        file.close()
        print("Data saved to: {}".format(filepath))

    def load_from_file(self, filepath):
        """Load data from a previously saved file."""
        if not os.path.exists(filepath):
            print("No previous data found. Starting fresh.")
            return

        file = open(filepath, "r")
        lines = file.readlines()
        file.close()

        # Clean up lines (remove newline characters)
        lines = [line.strip() for line in lines]

        i = 0
        while i < len(lines):
            line = lines[i]

            # Load balance
            if line == "BALANCE":
                i += 1
                self.account_balance = float(lines[i])

            # Load products
            elif line == "PRODUCTS":
                i += 1
                while lines[i] != "END_PRODUCTS":
                    parts = lines[i].split("|")
                    name = parts[0]
                    price = float(parts[1])
                    quantity = int(float(parts[2]))
                    self.products[name] = {"price": price, "quantity": quantity}
                    i += 1

            # Load sales
            elif line == "SALES":
                i += 1
                while lines[i] != "END_SALES":
                    parts = lines[i].split("|")
                    name = parts[0]
                    qty = int(float(parts[1]))
                    self.sales[name] = qty
                    i += 1

            # Load operations
            elif line == "OPERATIONS":
                i += 1
                while lines[i] != "END_OPERATIONS":
                    parts = lines[i].split("|")
                    if parts[0] == "balance":
                        self.operations.append(("balance", float(parts[1])))
                    elif parts[0] == "sale":
                        self.operations.append(("sale", parts[1], float(parts[2]), int(float(parts[3]))))
                    elif parts[0] == "purchase":
                        self.operations.append(("purchase", parts[1], float(parts[2]), int(float(parts[3]))))
                    i += 1

            i += 1

        print("Previous data loaded successfully!")
        print("Current balance: {}".format(self.account_balance))


# Create the manager instance
manager = Manager()

# The file where data is saved and loaded from
DATA_FILE = "accounting_data.txt"

# LOAD previous data when program starts
manager.load_from_file(DATA_FILE)


# ============================================================
# Actions registered via decorators
# ============================================================

@manager.assign("balance")
def balance(mgr):
    """Add or subtract from account balance."""
    try:
        amount = float(input("Enter amount to add or subtract (negative, positive): "))
    except ValueError:
        print("Invalid amount.")
        return
    mgr.operations.append(("balance", amount))
    mgr.account_balance += amount
    print("Balance updated: {}".format(mgr.account_balance))


@manager.assign("sale")
def sale(mgr):
    """Sell a product from the warehouse."""
    product = input("Enter product name: ")
    if not product:
        print("Product name cannot be empty.")
        return

    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price per unit: "))
    except ValueError:
        print("Invalid quantity or price.")
        return

    if quantity <= 0:
        print("Quantity must be a positive number.")
        return
    if price < 0:
        print("Price cannot be negative.")
        return
    if product not in mgr.products:
        print("'{}' is not in the warehouse.".format(product))
        return
    if mgr.products[product]["quantity"] < quantity:
        print("Not enough stock. Available: {}".format(mgr.products[product]["quantity"]))
        return

    revenue = price * quantity
    mgr.account_balance += revenue
    mgr.products[product]["quantity"] -= quantity

    if product in mgr.sales:
        mgr.sales[product] += quantity
    else:
        mgr.sales[product] = quantity

    if mgr.products[product]["quantity"] == 0:
        del mgr.products[product]

    mgr.operations.append(("sale", product, price, quantity))
    print("Sold {} x '{}'. Revenue: {}".format(quantity, product, revenue))
    print("Current balance: {}".format(mgr.account_balance))


@manager.assign("purchase")
def purchase(mgr):
    """Purchase a product and add to warehouse."""
    product = input("Enter product name: ")
    if not product:
        print("Product name cannot be empty.")
        return

    try:
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Invalid quantity.")
        return

    if quantity <= 0:
        print("Quantity must be a positive number.")
        return

    try:
        price = float(input("Enter price per unit: "))
    except ValueError:
        print("Invalid price.")
        return

    if price < 0:
        print("Price cannot be negative.")
        return

    cost = price * quantity

    if mgr.account_balance - cost < 0:
        print("Not enough funds! Balance: {}, Cost: {}".format(mgr.account_balance, cost))
        return

    mgr.account_balance -= cost

    if product in mgr.products:
        mgr.products[product]["quantity"] += quantity
        mgr.products[product]["price"] = price
    else:
        mgr.products[product] = {"price": price, "quantity": quantity}

    mgr.operations.append(("purchase", product, price, quantity))
    print("Purchased {} x '{}'. Cost: {}".format(quantity, product, cost))
    print("Current balance: {}".format(mgr.account_balance))


@manager.assign("account")
def account(mgr):
    """Display current account balance."""
    print("Current balance: {}".format(mgr.account_balance))


@manager.assign("list")
def list_products(mgr):
    """List all products in warehouse and sales history."""
    if not mgr.products:
        print("Warehouse is empty.")
    else:
        for product, info in mgr.products.items():
            print("{} - Price: {}, Quantity: {}".format(product, info["price"], info["quantity"]))

    if mgr.sales:
        print("\nTotal products sold:")
        for product, qty in mgr.sales.items():
            print("  {}: {} units".format(product, qty))


@manager.assign("warehouse")
def warehouse(mgr):
    """Look up a specific product in the warehouse."""
    product = input("Enter product name: ")

    if product in mgr.products:
        print("{} - Price: {}, Quantity: {}".format(
            product, mgr.products[product]["price"], mgr.products[product]["quantity"]))
    else:
        print("'{}' is not in the warehouse.".format(product))


@manager.assign("review")
def review(mgr):
    """Review operation history with optional range."""
    if not mgr.operations:
        print("No operations recorded yet.")
        return

    from_text = input("From index (press Enter for start): ")
    to_text = input("To index (press Enter for end): ")

    if from_text == "":
        from_idx = 0
    else:
        try:
            from_idx = int(from_text)
        except ValueError:
            print("Invalid index.")
            return

    if to_text == "":
        to_idx = len(mgr.operations)
    else:
        try:
            to_idx = int(to_text)
        except ValueError:
            print("Invalid index.")
            return

    if from_idx < 0:
        from_idx = 0
    if to_idx > len(mgr.operations):
        to_idx = len(mgr.operations)
    if from_idx >= to_idx:
        print("Invalid range.")
        return

    for i in range(from_idx, to_idx):
        op = mgr.operations[i]
        if op[0] == "balance":
            print("[{}] Balance: {}".format(i, op[1]))
        elif op[0] == "sale":
            print("[{}] Sale: {} x '{}' at {}".format(i, op[3], op[1], op[2]))
        elif op[0] == "purchase":
            print("[{}] Purchase: {} x '{}' at {}".format(i, op[3], op[1], op[2]))


# ============================================================
# Main menu loop
# ============================================================

MENU_OPTIONS = {
    "0": "end",
    "1": "balance",
    "2": "sale",
    "3": "purchase",
    "4": "account",
    "5": "list",
    "6": "warehouse",
    "7": "review"
}

while True:
    print("\n--- MENU ---")
    print("0. end")
    print("1. balance")
    print("2. sale")
    print("3. purchase")
    print("4. account")
    print("5. list")
    print("6. warehouse")
    print("7. review")

    choice = input("Choose option: ").strip()

    if choice not in MENU_OPTIONS:
        print("Wrong option")
        continue

    action_name = MENU_OPTIONS[choice]

    if action_name == "end":
        # SAVE data before exiting
        manager.save_to_file(DATA_FILE)
        print("Thank you! Bye :)")
        break

    print(action_name)
    manager.execute(action_name)

