# budgetmaster/expense/entry.py

from .base_transaction import BaseTransaction
from budgetmaster.analysis.utils import validate_amount

# in-memory storage
_expenses = []
_next_expense_id = 1


class Expense(BaseTransaction):
    """
    Expense class that inherits from BaseTransaction and adds a category
    and simple tag support. And, it represents a single expense item.
    """

    def __init__(self, category, amount, date, description=""):
        # call the parent __init__
        BaseTransaction.__init__(self, amount, date, description)
        self.category = category
        self.tags = []

    def is_over_budget(self, category_limit):
        """
        Check if this expense is larger than the given category limit.
        """
        return self.amount > category_limit

    def add_tag(self, tag):
        """
        Add a tag string to this expense (if not already present).
        """
        if tag not in self.tags:
            self.tags.append(tag)


def add_expense(category, amount, date, description=""):
    """
    Create an expense object, store it in the in-memory list, and return
    the stored dictionary record.
    """
    global _next_expense_id
    
    # make sure the amountes are  non-negative 
    validate_amount(amount)

    expense = Expense(category, amount, date, description)
    record = expense.to_dict()
    record["category"] = expense.category
    record["tags"] = list(expense.tags)
    record["expense_id"] = _next_expense_id

    _expenses.append(record)
    _next_expense_id += 1
    return record


def get_all_expenses():
    """
    Return a list of all stored expense records.
    """
    return list(_expenses)


def delete_expense(expense_id):
    """
    Delete an expense by its id. If the id does not exist, then do nothing.
    """
    global _expenses
    new_list = []
    for rec in _expenses:
        if rec.get("expense_id") != expense_id:
            new_list.append(rec)
    _expenses = new_list


def total_by_category():
    """
    Compute total expense amount for each category.

    Returns
    -------
    dict
        Keys are categories, values are total expense amounts.
    """
    totals = {}
    for rec in _expenses:
        category = rec.get("category", "uncategorized")
        amount = rec.get("amount", 0.0)
        if category not in totals:
            totals[category] = 0.0
        totals[category] += amount
    return totals

