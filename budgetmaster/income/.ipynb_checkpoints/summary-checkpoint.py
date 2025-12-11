# budgetmaster/income/summary.py

from budgetmaster.income.entry import get_all_incomes


def filter_by_month(month):
    """
    Helper: pick incomes whose date starts with the given month.

    month format: 'YYYY-MM', for example '2025-11'
    """
    all_incomes = get_all_incomes()
    result = []
    for rec in all_incomes:
        date = rec.get("date", "")
        if isinstance(date, str) and date.startswith(month):
            result.append(rec)
    return result


def total_monthly_income(month):
    """
    Calculate total income for a given month.

    Parameters
    ----------
    month : str
        Month in 'YYYY-MM' format, for example '2025-11'

    Returns
    -------
    float
        Sum of all income amounts for that month.
    """
    records = filter_by_month(month)
    total = 0.0
    for rec in records:
        total += rec.get("amount", 0.0)
    return float(total)


def average_monthly_income():
    """
    Compute the average monthly income across all months in the data.

    Returns
    -------
    float
        Average monthly income. Returns 0.0 if no data.
    """
    all_incomes = get_all_incomes()
    if not all_incomes:
        return 0.0

    month_totals = {}

    for rec in all_incomes:
        date = rec.get("date", "")
        if isinstance(date, str) and len(date) >= 7:
            month = date[:7]  # 'YYYY-MM'
            amount = rec.get("amount", 0.0)
            if month not in month_totals:
                month_totals[month] = 0.0
            month_totals[month] += amount

    if not month_totals:
        return 0.0

    total = 0.0
    for m in month_totals:
        total += month_totals[m]

    return float(total / len(month_totals))


def income_by_source():
    """
    Group total income by source.

    Returns
    -------
    dict
        Keys are sources, values are total amounts.
    """
    all_incomes = get_all_incomes()
    result = {}
    for rec in all_incomes:
        source = rec.get("source", "unknown")
        amount = rec.get("amount", 0.0)
        if source not in result:
            result[source] = 0.0
        result[source] += amount
    return result

