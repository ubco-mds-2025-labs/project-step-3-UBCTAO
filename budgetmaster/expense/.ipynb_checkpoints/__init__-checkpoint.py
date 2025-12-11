# budgetmaster/expense/__init__.py
"""
Expense sub-package.

Modules:
- base_transaction : BaseTransaction class. It defines a basic transaction class with: amount, date, and description. It also includes update and dictionary methods. This class is the parent for all expense objects.
- entry            : Expense class (inherits from BaseTransaction) and simple helper functions for expenses, such as add expenses, delete expenses, view all expenses,check whether spending goes over a budget limit. Users can also add tags to organize spending.
"""