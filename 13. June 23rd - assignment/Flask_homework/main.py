from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# Starting data
account_balance = 0.0
warehouse = []
history = []

# File path - always looks in the same folder as main.py
FILE_PATH = os.path.join(os.path.dirname(__file__), "history.txt")


# ---- MAIN PAGE ----
@app.route("/")
def main_page():
    return render_template("index.html", balance=account_balance, warehouse=warehouse)


# ---- BALANCE FORM ----
@app.route("/balance", methods=["POST"])
def change_balance():
    global account_balance

    try:
        amount = float(request.form["form_amount"])
    except (ValueError, KeyError):
        return "Error: Invalid amount entered."

    account_balance += amount
    history.append("Balance changed by: " + str(amount))
    save_history()

    return redirect("http://127.0.0.1:5000")


# ---- PURCHASE FORM ----
@app.route("/purchase", methods=["POST"])
def purchase():
    global account_balance

    try:
        product_name = request.form["form_product"]
        price = float(request.form["form_price"])
        quantity = int(request.form["form_quantity"])
    except (ValueError, KeyError):
        return "Error: Invalid data entered."

    total_cost = price * quantity

    if total_cost > account_balance:
        return "Error: Not enough funds."

    if not product_name or quantity <= 0 or price <= 0:
        return "Error: Invalid values."

    account_balance -= total_cost
    warehouse.append({"name": product_name, "price": price, "quantity": quantity})
    history.append("Purchased: " + product_name + " x" + str(quantity) + " for " + str(total_cost))
    save_history()

    return redirect("http://127.0.0.1:5000")


# ---- SALE FORM ----
@app.route("/sale", methods=["POST"])
def sale():
    global account_balance

    try:
        product_name = request.form["form_product"]
        price = float(request.form["form_price"])
        quantity = int(request.form["form_quantity"])
    except (ValueError, KeyError):
        return "Error: Invalid data entered."

    if not product_name or quantity <= 0 or price <= 0:
        return "Error: Invalid values."

    for item in warehouse:
        if item["name"] == product_name:
            if item["quantity"] >= quantity:
                item["quantity"] -= quantity
                account_balance += price * quantity
                history.append("Sold: " + product_name + " x" + str(quantity) + " for " + str(price * quantity))
                save_history()
                return redirect("http://127.0.0.1:5000")
            else:
                return "Error: Not enough stock."

    return "Error: Product not found in warehouse."


# ---- HISTORY PAGE ----
@app.route("/history/")
@app.route("/history/<int:line_from>/<int:line_to>/")
def show_history(line_from=None, line_to=None):
    if line_from is not None and line_to is not None:
        display_history = history[line_from:line_to]
    else:
        display_history = history

    return render_template("history.html", history=display_history)


# ---- FILE READ/WRITE ----
def save_history():
    try:
        with open(FILE_PATH, "w") as file:
            for line in history:
                file.write(line + "\n")
    except IOError:
        print("Error: Could not write to file.")


def load_history():
    try:
        with open(FILE_PATH, "r") as file:
            for line in file:
                history.append(line.strip())
    except FileNotFoundError:
        print("No history file found. Starting fresh.")
    except IOError:
        print("Error: Could not read file.")


# Load history when app starts
load_history()

if __name__ == "__main__":
    app.run(debug=True)
