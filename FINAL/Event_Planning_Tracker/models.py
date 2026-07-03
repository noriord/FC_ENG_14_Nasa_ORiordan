
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date_from = db.Column(db.String(50), nullable=False)
    date_to = db.Column(db.String(50), nullable=True)
    expected_attendees = db.Column(db.Integer, nullable=True)
    actual_attendees = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Planned')

    @property
    def date_display(self):
        if self.date_to:
            return f"{self.date_from} → {self.date_to}"
        return self.date_from

    def __repr__(self):
        return f"<Event {self.name} - {self.status}>"


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_budget = db.Column(db.Float, nullable=False, default=0.0)
    spent = db.Column(db.Float, nullable=False, default=0.0)

    @property
    def remaining(self):
        return self.total_budget - self.spent

    def __repr__(self):
        return f"<Budget Total: {self.total_budget}, Spent: {self.spent}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Location {self.name}>"


class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gbp_to_eur = db.Column(db.Float, nullable=False, default=1.17)

    def __repr__(self):
        return f"<ExchangeRate GBP→EUR: {self.gbp_to_eur}>"


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    original_amount = db.Column(db.Float, nullable=True)
    original_currency = db.Column(db.String(10), nullable=False, default='EUR')
    category = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    event = db.relationship('Event', backref='expenses')

    def __repr__(self):
        return f"<Expense {self.description}: {self.amount}>"


class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<Log {self.type}: {self.description}>"

