# budgetmaster/analysis/utils.py

class InvalidAmountError(ValueError):
    """
    Custom error raised when a numeric amount is invalid (for example,
    negative). It subclasses ValueError so any existing code that
    expects ValueError will still work.
    """
    pass


def categorize_expense(expense):
    """
    Try to guess a category for the expense based on its description.

    Parameters
    ----------
    expense : dict

    Returns
    -------
    str
        Category name.
    """
    # if a category already exists, keep it
    if "category" in expense and expense["category"]:
        return expense["category"]

    desc = str(expense.get("description", "")).lower()

    if "rent" in desc or "mortgage" in desc:
        return "housing"
    if "uber" in desc or "bus" in desc or "train" in desc or "gas" in desc:
        return "transportation"
    if "grocery" in desc or "restaurant" in desc or "coffee" in desc:
        return "food"

    return "other"


def format_currency(amount):
    """
    Format a number as a simple currency string, for example:
    1234.5 -> '$1234.50'
    """
    return "${:.2f}".format(float(amount))


def validate_amount(amount):
    """
    Check that a number is non-negative.

    Parameters
    ----------
    amount : float or int

    Raises
    ------
    InvalidAmountError
        If the amount is negative.
    """
    if amount < 0:
        # user-defined exception I created it for project step 3 
        raise InvalidAmountError("Amount must be non-negative.")




