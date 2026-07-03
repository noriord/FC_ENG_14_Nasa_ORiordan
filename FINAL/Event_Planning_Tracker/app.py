
from flask import Flask, render_template, request, redirect, url_for
from models import db, Event, Budget, Expense, ActivityLog, Category, Location, ExchangeRate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'

db.init_app(app)


# Custom filter to format numbers with commas and 2 decimal places
@app.template_filter('currency')
def currency_format(value):
    return f"{value:,.2f}"


with app.app_context():
    db.create_all()
    # Initialise budget if it doesn't exist yet
    if not db.session.query(Budget).first():
        db.session.add(Budget(total_budget=0.0, spent=0.0))
        db.session.commit()
    # Initialise default categories if none exist
    if not db.session.query(Category).first():
        default_categories = [
            'Committee Related',
            'Party Related',
            'TM Engagement',
            'Prizes',
            'SWAG',
            'Others'
        ]
        for cat in default_categories:
            db.session.add(Category(name=cat))
        db.session.commit()
    # Initialise default locations if none exist
    if not db.session.query(Location).first():
        default_locations = [
            'Cork',
            'Dublin',
            'Edinburgh',
            'IRL + EDI'
        ]
        for loc in default_locations:
            db.session.add(Location(name=loc))
        db.session.commit()
    # Initialise exchange rate if it doesn't exist
    if not db.session.query(ExchangeRate).first():
        db.session.add(ExchangeRate(gbp_to_eur=1.17))
        db.session.commit()


@app.route('/')
def index():
    try:
        # Get EVENT sorting parameters
        sort_by = request.args.get('sort_by', 'date_from')
        sort_order = request.args.get('sort_order', 'asc')

        # Build event query with sorting
        if sort_by == 'name':
            sort_column = Event.name
        elif sort_by == 'status':
            sort_column = Event.status
        elif sort_by == 'location':
            sort_column = Event.location
        else:
            sort_column = Event.date_from

        if sort_order == 'desc':
            events = db.session.query(Event).order_by(sort_column.desc()).all()
        else:
            events = db.session.query(Event).order_by(sort_column.asc()).all()

        # Get EXPENSE sorting parameters
        exp_sort_by = request.args.get('exp_sort_by', 'timestamp')
        exp_sort_order = request.args.get('exp_sort_order', 'desc')

        # Build expense query with sorting
        if exp_sort_by == 'amount':
            exp_sort_column = Expense.amount
        elif exp_sort_by == 'category':
            exp_sort_column = Expense.category
        else:
            exp_sort_column = Expense.timestamp

        if exp_sort_order == 'desc':
            expenses = db.session.query(Expense).order_by(exp_sort_column.desc()).all()
        else:
            expenses = db.session.query(Expense).order_by(exp_sort_column.asc()).all()

        active_events = db.session.query(Event).filter(Event.status != 'Completed').all()
        budget = db.session.query(Budget).first()
        categories = db.session.query(Category).all()
        locations = db.session.query(Location).all()
        exchange_rate = db.session.query(ExchangeRate).first()
        return render_template('index.html', events=events, active_events=active_events, budget=budget, expenses=expenses, categories=categories, locations=locations, exchange_rate=exchange_rate, sort_by=sort_by, sort_order=sort_order, exp_sort_by=exp_sort_by, exp_sort_order=exp_sort_order)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/activity/')
def activity():
    try:
        logs = db.session.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).all()
        return render_template('activity.html', logs=logs)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/settings')
def settings():
    try:
        categories = db.session.query(Category).all()
        locations = db.session.query(Location).all()
        exchange_rate = db.session.query(ExchangeRate).first()
        return render_template('settings.html', categories=categories, locations=locations, exchange_rate=exchange_rate)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/add_event', methods=['POST'])
def add_event():
    try:
        name = request.form['event_name']
        location = request.form['location']
        date_from = request.form['date_from']
        date_to = request.form.get('date_to', '').strip()
        expected_attendees = request.form.get('expected_attendees', '').strip()

        # date_to is optional
        if not date_to:
            date_to = None

        # expected_attendees is optional
        if expected_attendees:
            expected_attendees = int(expected_attendees)
            if expected_attendees < 0:
                return render_template('error.html', message="Expected attendees cannot be negative.")
        else:
            expected_attendees = None

        event = Event(
            name=name,
            location=location,
            date_from=date_from,
            date_to=date_to,
            expected_attendees=expected_attendees
        )
        db.session.add(event)

        # Log activity
        date_display = f"{date_from} → {date_to}" if date_to else date_from
        db.session.add(ActivityLog(
            type='event_created',
            description=f'Created event: {name} at {location} on {date_display}'
        ))
        db.session.commit()

    except ValueError:
        db.session.rollback()
        return render_template('error.html', message="Invalid input. Please enter valid numbers.")
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('index'))


@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    try:
        event = db.session.query(Event).filter_by(id=event_id).first()
        if not event:
            return render_template('error.html', message="Event not found.")

        if request.method == 'GET':
            locations = db.session.query(Location).all()
            return render_template('edit_event.html', event=event, locations=locations)

        # POST - update the event
        old_name = event.name
        event.name = request.form['event_name']
        event.location = request.form['location']
        event.date_from = request.form['date_from']
        date_to = request.form.get('date_to', '').strip()
        event.date_to = date_to if date_to else None

        expected_attendees = request.form.get('expected_attendees', '').strip()
        if expected_attendees:
            event.expected_attendees = int(expected_attendees)
        else:
            event.expected_attendees = None

        actual_attendees = request.form.get('actual_attendees', '').strip()
        if actual_attendees:
            event.actual_attendees = int(actual_attendees)
        else:
            event.actual_attendees = None

        # Log activity
        db.session.add(ActivityLog(
            type='event_edited',
            description=f'Edited event: "{old_name}" → "{event.name}" ({event.location}, {event.date_display})'
        ))
        db.session.commit()

    except ValueError:
        db.session.rollback()
        return render_template('error.html', message="Invalid input. Please enter valid numbers.")
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('index'))


@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    try:
        event = db.session.query(Event).filter_by(id=event_id).first()
        if not event:
            return render_template('error.html', message="Event not found.")

        # Check if event has expenses — refund them to budget
        budget = db.session.query(Budget).first()
        total_refund = sum(e.amount for e in event.expenses)
        for expense in event.expenses:
            budget.spent -= expense.amount
            db.session.delete(expense)

        # Log activity
        db.session.add(ActivityLog(
            type='event_deleted',
            description=f'Deleted event: {event.name} ({event.location}, {event.date_display}). Refunded €{total_refund:,.2f} to budget.'
        ))

        db.session.delete(event)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('index'))


@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        event_id = int(request.form['event_id'])
        description = request.form['description']
        amount_input = float(request.form['amount'])
        category = request.form['category']
        currency = request.form['currency']

        if amount_input <= 0:
            return render_template('error.html', message="Amount must be positive.")

        # Check event exists
        event = db.session.query(Event).filter_by(id=event_id).first()
        if not event:
            return render_template('error.html', message="Event not found.")

        # Convert if GBP
        if currency == 'GBP':
            exchange_rate = db.session.query(ExchangeRate).first()
            eur_amount = round(amount_input * exchange_rate.gbp_to_eur, 2)
            original_amount = amount_input
            original_currency = 'GBP'
        else:
            eur_amount = amount_input
            original_amount = amount_input
            original_currency = 'EUR'

        # Check budget
        budget = db.session.query(Budget).first()
        if eur_amount > budget.remaining:
            return render_template('error.html', message=f"Not enough budget. Remaining: €{budget.remaining:,.2f}")

        # Add expense
        expense = Expense(
            event_id=event_id,
            description=description,
            amount=eur_amount,
            original_amount=original_amount,
            original_currency=original_currency,
            category=category
        )
        db.session.add(expense)

        # Update budget spent
        budget.spent += eur_amount

        # Log activity
        if currency == 'GBP':
            db.session.add(ActivityLog(
                type='expense_added',
                description=f'Added expense: {description} (£{amount_input:,.2f} → €{eur_amount:,.2f}) for {event.name} [{category}]'
            ))
        else:
            db.session.add(ActivityLog(
                type='expense_added',
                description=f'Added expense: {description} (€{eur_amount:,.2f}) for {event.name} [{category}]'
            ))
        db.session.commit()

    except ValueError:
        db.session.rollback()
        return render_template('error.html', message="Invalid input. Please enter valid numbers.")
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('index'))


@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    try:
        expense = db.session.query(Expense).filter_by(id=expense_id).first()
        if not expense:
            return render_template('error.html', message="Expense not found.")

        if request.method == 'GET':
            events = db.session.query(Event).all()
            categories = db.session.query(Category).all()
            exchange_rate = db.session.query(ExchangeRate).first()
            return render_template('edit_expense.html', expense=expense, events=events, categories=categories, exchange_rate=exchange_rate)

        # POST - update the expense
        old_amount = expense.amount
        old_description = expense.description
        old_category = expense.category

        expense.event_id = int(request.form['event_id'])
        expense.description = request.form['description']
        amount_input = float(request.form['amount'])
        expense.category = request.form['category']
        currency = request.form['currency']

        if amount_input <= 0:
            return render_template('error.html', message="Amount must be positive.")

        # Convert if GBP
        if currency == 'GBP':
            exchange_rate = db.session.query(ExchangeRate).first()
            expense.amount = round(amount_input * exchange_rate.gbp_to_eur, 2)
            expense.original_amount = amount_input
            expense.original_currency = 'GBP'
        else:
            expense.amount = amount_input
            expense.original_amount = amount_input
            expense.original_currency = 'EUR'

        # Update budget (remove old amount, add new amount)
        budget = db.session.query(Budget).first()
        budget.spent = budget.spent - old_amount + expense.amount

        # Log activity
        db.session.add(ActivityLog(
            type='expense_edited',
            description=f'Edited expense: "{old_description}" (€{old_amount:,.2f}, {old_category}) → "{expense.description}" (€{expense.amount:,.2f}, {expense.category})'
        ))
        db.session.commit()

    except ValueError:
        db.session.rollback()
        return render_template('error.html', message="Invalid input. Please enter valid numbers.")
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('index'))


@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    try:
        expense = db.session.query(Expense).filter_by(id=expense_id).first()
        if not expense:
            return render_template('error.html', message="Expense not found.")

        # Update budget (give back the money)
        budget = db.session.query(Budget).first()
        budget.spent -= expense.amount

        # Log activity
        db.session.add(ActivityLog(
            type='expense_deleted',
            description=f'Deleted expense: {expense.description} (€{expense.amount:,.2f}) from {expense.event.name} [{expense.category}]'
        ))

        db.session.delete(expense)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('index'))


@app.route('/add_category', methods=['POST'])
def add_category():
    try:
        name = request.form['category_name'].strip()

        if not name:
            return render_template('error.html', message="Category name cannot be empty.")

        existing = db.session.query(Category).filter_by(name=name).first()
        if existing:
            return render_template('error.html', message=f"Category '{name}' already exists.")

        db.session.add(Category(name=name))

        db.session.add(ActivityLog(
            type='category_added',
            description=f'New category added: {name}'
        ))
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('settings'))


@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    try:
        category = db.session.query(Category).filter_by(id=category_id).first()
        if not category:
            return render_template('error.html', message="Category not found.")

        db.session.add(ActivityLog(
            type='category_deleted',
            description=f'Category deleted: {category.name}'
        ))

        db.session.delete(category)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('settings'))


@app.route('/add_location', methods=['POST'])
def add_location():
    try:
        name = request.form['location_name'].strip()

        if not name:
            return render_template('error.html', message="Location name cannot be empty.")

        existing = db.session.query(Location).filter_by(name=name).first()
        if existing:
            return render_template('error.html', message=f"Location '{name}' already exists.")

        db.session.add(Location(name=name))

        db.session.add(ActivityLog(
            type='location_added',
            description=f'New location added: {name}'
        ))
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('settings'))


@app.route('/delete_location/<int:location_id>', methods=['POST'])
def delete_location(location_id):
    try:
        location = db.session.query(Location).filter_by(id=location_id).first()
        if not location:
            return render_template('error.html', message="Location not found.")

        db.session.add(ActivityLog(
            type='location_deleted',
            description=f'Location deleted: {location.name}'
        ))

        db.session.delete(location)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('settings'))


@app.route('/update_exchange_rate', methods=['POST'])
def update_exchange_rate():
    try:
        new_rate = float(request.form['gbp_to_eur'])

        if new_rate <= 0:
            return render_template('error.html', message="Exchange rate must be positive.")

        exchange_rate = db.session.query(ExchangeRate).first()
        old_rate = exchange_rate.gbp_to_eur
        exchange_rate.gbp_to_eur = new_rate

        db.session.add(ActivityLog(
            type='rate_updated',
            description=f'Exchange rate updated: £1 = €{old_rate} → €{new_rate}'
        ))
        db.session.commit()

    except ValueError:
        db.session.rollback()
        return render_template('error.html', message="Invalid input. Please enter a valid number.")
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('settings'))


@app.route('/update_status', methods=['POST'])
def update_status():
    try:
        event_id = int(request.form['event_id'])
        new_status = request.form['status']
        actual_attendees = request.form.get('actual_attendees', '').strip()

        event = db.session.query(Event).filter_by(id=event_id).first()
        if not event:
            return render_template('error.html', message="Event not found.")

        old_status = event.status
        event.status = new_status

        if actual_attendees:
            event.actual_attendees = int(actual_attendees)

        db.session.add(ActivityLog(
            type='status_change',
            description=f'{event.name}: {old_status} → {new_status}'
        ))
        db.session.commit()

    except ValueError:
        db.session.rollback()
        return render_template('error.html', message="Invalid input.")
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=str(e))

    return redirect(url_for('index'))


@app.route('/update_budget', methods=['POST'])
def update_budget():
    try:
        total_budget = float(request.form['total_budget'])

        budget = db.session.query(Budget).first()
        budget.total_budget = total_budget

        db.session.add(ActivityLog(
            type='budget_update',
            description=f'Total budget set to €{total_budget:,.2f}'
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
            logs = db.session.query(ActivityLog).all()[line_from:line_to]
        else:
            logs = db.session.query(ActivityLog).all()
        return render_template('history.html', logs=logs)
    except Exception as e:
        return render_template('error.html', message=str(e))


if __name__ == '__main__':
    app.run(debug=True)

