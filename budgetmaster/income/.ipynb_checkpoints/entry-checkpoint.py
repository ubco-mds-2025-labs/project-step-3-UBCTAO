# budgetmaster/income/entry.py

from budgetmaster.analysis.utils import validate_amount
# simple in-memory storage (list of dictionaries). 
# since this project only needs lightweight examples.

incomes = []
next_income_id = 1



def add_income(source, amount, date):
    """
    Add a new income record.

    Parameters
    ----------
    source : str
        Where the income comes from. For example, come from salary, freelance, etc.
    amount : float
        Income amount (must be non-negative).
    date : str
        Date string, for example '2025-12-02'.

    Returns
    -------
    dict
        The created income record.
    """
    global next_income_id

    if amount < 0:
        raise ValueError("Income amount must be non-negative.")

    record = {
        "income_id": next_income_id,
        "source": source,
        "amount": float(amount),
        "date": date,
    }
    incomes.append(record)
    next_income_id += 1
    return record


def update_income(income_id, new_source=None, new_amount=None, new_date=None):
    """
    Update an existing income record. Returns the updated record.

    Raises
    ------
    ValueError
        If the given income_id is not found.
    """
    for rec in incomes:
        if rec["income_id"] == income_id:
            if new_source is not None:
                rec["source"] = new_source
            if new_amount is not None:
                # we want to make sure updated amounts are also valid
                validate_amount(new_amount)
                rec["amount"] = float(new_amount)
            if new_date is not None:
                rec["date"] = new_date
            return rec

    raise ValueError("No income found with id = {}".format(income_id))


def delete_income(income_id):
    """
    Delete an income record by id. If the id does not exist, then nothing happens.
    """
    global incomes
    new_list = []
    for rec in incomes:
        if rec["income_id"] != income_id:
            new_list.append(rec)
    incomes = new_list


def get_all_incomes():
    """
    Return a list of all current income records.
    """
    # return a shallow copy to avoid accidental external changes
    return list(incomes)




