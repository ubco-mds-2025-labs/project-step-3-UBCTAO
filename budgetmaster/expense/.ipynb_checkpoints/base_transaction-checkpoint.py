
# budgetmaster/expense/base_transaction.py

class BaseTransaction:
    """
    Base class for transaction-like objects. 

    Attributes
    ----------
    amount : float
    date : str
    description : str
    """

    def __init__(self, amount, date, description=""):
        if amount < 0:
            raise ValueError("Amount must be non-negative.")
        self.amount = float(amount)
        self.date = date
        self.description = description

    def update(self, new_amount=None, new_date=None, new_description=None):
        """
        Update the transaction fields in-place.
        """
        if new_amount is not None:
            if new_amount < 0:
                raise ValueError("Amount must be non-negative.")
            self.amount = float(new_amount)
        if new_date is not None:
            self.date = new_date
        if new_description is not None:
            self.description = new_description

    def to_dict(self):
        """
        Convert this transaction to a dictionary.
        """
        return {
            "amount": self.amount,
            "date": self.date,
            "description": self.description,
        }
