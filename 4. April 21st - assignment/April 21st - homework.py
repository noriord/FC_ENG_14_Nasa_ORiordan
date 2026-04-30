# Company Account & Warehouse Simulator

balance = 0.0
warehouse = {}
operations = []

commands = ["balance", "sale", "purchase", "account", "list", "warehouse", "review", "end"]

while True:
    # Show menu
    print("*" * 40)
    print("What would you like to do?")
    print("*" * 40)
    for selection in range(len(commands)):
        print("  {} - {}".format(selection + 1, commands[selection]))
    print("*" * 40)

    choice = input("Pick a number (1-8): ")

    # Convert number to command
    try:
        number = int(choice)
        if number < 1 or number > 8:
            print("Please pick 1-8.")
            continue
        command = commands[number - 1]
    except ValueError:
        print("Please enter a number.")
        continue

    # ---- BALANCE ----
    if command == "balance":
        try:
            amount = float(input("Enter amount (negative to subtract): "))
        except ValueError:
            print("Invalid amount.")
            continue

        balance = balance + amount
        operations.append(("balance", amount))
        print("Balance updated: {}".format(balance))

    # ---- SALE ----
    elif command == "sale":
        product = input("Enter product name: ")
        if not product:
            print("Product name cannot be empty.")
            continue

        try:
            price = float(input("Enter price: "))
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid price or quantity.")
            continue

        if product not in warehouse:
            print("'{}' is not in the warehouse.".format(product))
            continue

        if warehouse[product]["quantity"] < quantity:
            print("Not enough stock. Available: {}".format(warehouse[product]["quantity"]))
            continue

        revenue = price * quantity
        balance = balance + revenue
        warehouse[product]["quantity"] = warehouse[product]["quantity"] - quantity

        if warehouse[product]["quantity"] == 0:
            del warehouse[product]

        operations.append(("sale", product, price, quantity))
        print("Sold {} x '{}'. Revenue: {}".format(quantity, product, revenue))
        print("Current balance: {}".format(balance))

    # ---- PURCHASE ----
    elif command == "purchase":
        product = input("Enter product name: ")
        if not product:
            print("Product name cannot be empty.")
            continue

        try:
            price = float(input("Enter price: "))
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid price or quantity.")
            continue

        cost = price * quantity

        if balance - cost < 0:
            print("Not enough funds! Balance: {}, Cost: {}".format(balance, cost))
            continue

        balance = balance - cost

        if product in warehouse:
            warehouse[product]["quantity"] = warehouse[product]["quantity"] + quantity
            warehouse[product]["price"] = price
        else:
            warehouse[product] = {"price": price, "quantity": quantity}

        operations.append(("purchase", product, price, quantity))
        print("Purchased {} x '{}'. Cost: {}".format(quantity, product, cost))
        print("Current balance: {}".format(balance))

    # ---- ACCOUNT ----
    elif command == "account":
        print("*" * 40)
        print("Current balance: {}".format(balance))
        print("*" * 40)

    # ---- LIST ----
    elif command == "list":
        if not warehouse:
            print("Warehouse is empty.")
        else:
            print("*" * 40)
            print("Warehouse inventory")
            print("*" * 40)
            for product, info in warehouse.items():
                print("{} - Price: {}, Quantity: {}".format(product, info["price"], info["quantity"]))
            print("*" * 40)

    # ---- WAREHOUSE ----
    elif command == "warehouse":
        product = input("Enter product name: ")

        if product in warehouse:
            print("{} - Price: {}, Quantity: {}".format(
                product, warehouse[product]["price"], warehouse[product]["quantity"]))
        else:
            print("'{}' is not in the warehouse.".format(product))

    # ---- REVIEW ----
    elif command == "review":
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

        print("*" * 40)
        for i in range(from_idx, to_idx):
            op = operations[i]
            if op == "balance":
                print("[{}] Balance: {}".format(i, op))
            elif op == "sale":
                print("[{}] Sale: {} x '{}' at {}".format(i, op, op, op))
            elif op == "purchase":
                print("[{}] Purchase: {} x '{}' at {}".format(i, op, op, op))
        print("*" * 40)

    # ---- END ----
    elif command == "end":
        print("Goodbye!")
        break
