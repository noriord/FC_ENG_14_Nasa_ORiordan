
from flask import Flask, render_template, request, redirect, url_for
from models import db, Product, Balance, Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounting.db'

db.init_app(app)

with app.app_context():
    db.create_all()
    # Initialise balance if it doesn't exist yet
    if not db.session.query(Balance).first():
        db.session.add(Balance(amount=0.0))
        db.session.commit()


@app.route('/')
def index():
    try:
        products = db.session.query(Product).all()
        balance = db.session.query(Balance).first().amount
        return render_template('index.html', products=products, balance=balance)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/purchase', methods=['POST'])
def purchase():
    try:
        name = request.form['product_name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        if quantity <= 0 or price <= 0:
            return render_template('error.html', message="Quantity and price must be positive.")

        # Check if we have enough balance
        balance = db.session.query(Balance).first()
        total_cost = quantity * price

        if total_cost > balance.amount:
            return render_template('error.html', message="Not enough funds for this purchase.")

        # Update or create product
        product = db.session.query(Product).filter_by(name=name).first()
        if product:
            product.quantity += quantity
        else:
            product = Product(name=name, quantity=quantity)
            db.session.add(product)

        # Deduct from balance
        balance.amount -= total_cost

        # Log transaction
        db.session.add(Transaction(
            type='purchase',
            description=f'Purchased {quantity} of {name} for {total_cost}'
        ))
        db.session.commit()

    except ValueError:
        db.session.rollback()
        return render_template('error.html', message="Invalid input. Please enter valid numbers.")
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('index'))


@app.route('/sale', methods=['POST'])
def sale():
    try:
        name = request.form['product_name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        if quantity <= 0 or price <= 0:
            return render_template('error.html', message="Quantity and price must be positive.")

        # Check if product exists and has enough stock
        product = db.session.query(Product).filter_by(name=name).first()
        if not product:
            return render_template('error.html', message=f"Product '{name}' not found.")
        if product.quantity < quantity:
            return render_template('error.html', message=f"Not enough stock. Available: {product.quantity}")

        # Update product quantity
        product.quantity -= quantity

        # Add to balance
        balance = db.session.query(Balance).first()
        total_income = quantity * price
        balance.amount += total_income

        # Log transaction
        db.session.add(Transaction(
            type='sale',
            description=f'Sold {quantity} of {name} for {total_income}'
        ))
        db.session.commit()

    except ValueError:
        db.session.rollback()
        return render_template('error.html', message="Invalid input. Please enter valid numbers.")
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('index'))


@app.route('/balance', methods=['POST'])
def change_balance():
    try:
        amount = float(request.form['amount'])

        balance = db.session.query(Balance).first()
        balance.amount += amount

        # Log transaction
        db.session.add(Transaction(
            type='balance_change',
            description=f'Balance changed by {amount}'
        ))
        db.session.commit()

    except ValueError:
        db.session.rollback()
        return render_template('error.html', message="Invalid input. Please enter a valid number.")
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('index'))


@app.route('/history/')
@app.route('/history/<int:line_from>/<int:line_to>/')
def history(line_from=None, line_to=None):
    try:
        if line_from is not None and line_to is not None:
            transactions = db.session.query(Transaction).all()[line_from:line_to]
        else:
            transactions = db.session.query(Transaction).all()
        return render_template('history.html', transactions=transactions)
    except Exception as e:
        return render_template('error.html', message=str(e))


if __name__ == '__main__':
    app.run(debug=True)

