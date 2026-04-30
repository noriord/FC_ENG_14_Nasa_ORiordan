
# Company Account & Warehouse Simulator

account_balance = 0.0  # Init account balance
products = {}  # Dictionary to store prod details
sales = {}  # Dict to store total products sold
operations = []  # List to log all operations
# initial_balance = 0.0  # To track initial value of the warehouse
# final_balance = 0.0  # TO track current value of the warehouse

while True:
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
        print("Thank you! Bye :)")
        break

    elif choice == 1:
        print("balance")
        try:
            amount = float(input("Enter amount to add or subtract (negative, positive): "))
        except ValueError:
            print("Invalid amount.")
            continue
        # Log operation in operations list
        operations.append(("balance", amount))
        # Update the balance
        account_balance = account_balance + amount
        # Print confirm
        print("Balance updated: {}".format(account_balance))

    elif choice == 2:
        print("sale")
        # Provide product name
        product = input("Enter product name: ")
        if not product:
            print("Product name cannot be empty.")
            continue

        # Enter quantity and price
        try:
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price per unit: "))
        except ValueError:
            print("Invalid quantity or price.")
            continue

        # Check if product exists in warehouse
        if product not in products:
            print("'{}' is not in the warehouse.".format(product))
            continue

        # Check if enough stock
        if products[product]["quantity"] < quantity:
            print("Not enough stock. Available: {}".format(products[product]["quantity"]))
            continue

        # Calculate sale revenue
        revenue = price * quantity

        # Update balance
        account_balance = account_balance + revenue

        # Update warehouse quantity
        products[product]["quantity"] = products[product]["quantity"] - quantity

        # Track total sales per product
        if product in sales:
            sales[product] = sales[product] + quantity
        else:
            sales[product] = quantity

        # Remove product if quantity reaches 0
        if products[product]["quantity"] == 0:
            del products[product]

        # Log operation in history
        operations.append(("sale", product, price, quantity))
        print("Sold {} x '{}'. Revenue: {}".format(quantity, product, revenue))
        print("Current balance: {}".format(account_balance))

    elif choice == 3:
        print("purchase")
        # Provide product name
        product = input("Enter product name: ")
        if not product:
            print("Product name cannot be empty.")
            continue

        # Enter quantity
        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid quantity.")
            continue

        # Enter price per quantity
        try:
            price = float(input("Enter price per unit: "))
        except ValueError:
            print("Invalid price.")
            continue

        # Calculate purchase total sum
        cost = price * quantity

        # Check if you can afford to buy it
        if account_balance - cost < 0:
            print("Not enough funds! Balance: {}, Cost: {}".format(account_balance, cost))
            continue

        # Update balance
        account_balance = account_balance - cost

        # Check if you have this product in dict products
        # If yes, then update quantity, if not add product
        if product in products:
            products[product]["quantity"] = products[product]["quantity"] + quantity
            products[product]["price"] = price
        else:
            products[product] = {"price": price, "quantity": quantity}

        # Log operation in history
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

