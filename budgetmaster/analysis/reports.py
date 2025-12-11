# budgetmaster/analysis/reports.py

import matplotlib.pyplot as plt
from collections import defaultdict


def monthly_balance(incomes, expenses):
    """
    Compute (income - expense) for each month.

    Parameters
    ----------
    incomes : list of dict
    expenses : list of dict

    Returns
    -------
    dict
        Keys are months (like '2025-11') and values are net balances.
    """
    income_by_month = {}
    expense_by_month = {}

    # sum incomes by month
    for rec in incomes:
        date = rec.get("date", "")
        if isinstance(date, str) and len(date) >= 7:
            month = date[:7]
            amount = rec.get("amount", 0.0)
            if month not in income_by_month:
                income_by_month[month] = 0.0
            income_by_month[month] += amount

    # sum expenses by month
    for rec in expenses:
        date = rec.get("date", "")
        if isinstance(date, str) and len(date) >= 7:
            month = date[:7]
            amount = rec.get("amount", 0.0)
            if month not in expense_by_month:
                expense_by_month[month] = 0.0
            expense_by_month[month] += amount

    # use sorted months so later plots look nicer
    all_months = sorted(set(income_by_month.keys()) | set(expense_by_month.keys()))
    result = {}

    for m in all_months:
        inc_total = income_by_month.get(m, 0.0)
        exp_total = expense_by_month.get(m, 0.0)
        result[m] = inc_total - exp_total

    return result


def savings_rate(incomes_total, expenses_total):
    """
    Compute savings rate = (income - expense) / income.

    Returns
    -------
    float
        The savings rate. If incomes_total <= 0, return 0.0.
    """
    if incomes_total <= 0:
        return 0.0
    return float((incomes_total - expenses_total) / incomes_total)


def generate_report(balance_data):
    """
    Generate a simple text report based on monthly balance data.

    Parameters
    ----------
    balance_data : dict
        Keys are 'YYYY-MM', values are net balances.

    Returns
    -------
    str
        Multi-line string report.
    """
    if not balance_data:
        return "No balance data available."

    lines = []
    lines.append("BudgetMaster Monthly Balance Report")
    lines.append("\n")

    for month in sorted(balance_data.keys()):
        balance = balance_data[month]
        if balance >= 0:
            status = "surplus"
        else:
            status = "deficit"
        lines.append("{}: {:.2f} ({})".format(month, balance, status))

    return "\n".join(lines)


def plot_monthly_balance(balance_data):
    """
    Visualize monthly net balance (income - expense) as a simple bar chart.

    Parameters
    ----------
    balance_data : dict
        Keys are months 'YYYY-MM', values are balance amounts.

    Notes
    -----
    This function is intentionally simple since the project
    only requires lightweight examples.
    """
    if not balance_data:
        print("No balance data to plot.")
        return

    # sort months so the x-axis is ordered
    months = sorted(balance_data.keys())
    values = [balance_data[m] for m in months]

    plt.figure(figsize=(7, 4))
    bars = plt.bar(months, values)

    # Add horizontal line at zero
    plt.axhline(0, color="black", linewidth=1)

    plt.title("Monthly Net Balance (Income - Expense)")
    plt.xlabel("Month")
    plt.ylabel("Balance Amount")

    # Add labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.0f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.show()


def plot_income_vs_expense(incomes, expenses):
    """
    Create a grouped bar chart comparing monthly income and monthly expenses.

    Parameters
    ----------
    incomes : list of dict
    expenses : list of dict

    Notes
    -----
    We use string slicing on the date (YYYY-MM) instead of full
    datetime parsing to keep the project simple.
    """

    # Group income by month
    monthly_income = defaultdict(float)
    for rec in incomes:
        date = rec.get("date", "")
        if isinstance(date, str) and len(date) >= 7:
            month = date[:7]
            monthly_income[month] += rec.get("amount", 0.0)

    # Group expense by month
    monthly_exp = defaultdict(float)
    for rec in expenses:
        date = rec.get("date", "")
        if isinstance(date, str) and len(date) >= 7:
            month = date[:7]
            monthly_exp[month] += rec.get("amount", 0.0)

    if not monthly_income and not monthly_exp:
        print("No income or expense data to plot.")
        return

    # Ensure consistent month order
    all_months = sorted(set(monthly_income.keys()) | set(monthly_exp.keys()))

    inc_vals = [monthly_income[m] for m in all_months]
    exp_vals = [monthly_exp[m] for m in all_months]

    x = range(len(all_months))
    width = 0.35

    plt.figure(figsize=(7, 4))
    plt.bar([i - width / 2 for i in x], inc_vals, width, label="Income")
    plt.bar([i + width / 2 for i in x], exp_vals, width, label="Expense")

    plt.xticks(list(x), all_months)
    plt.ylabel("Amount")
    plt.title("Monthly Income vs Expense")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_category_expense(expenses):
    """
    Plot a simple pie chart showing total expense amounts by category.

    Parameters
    ----------
    expenses : list of dict
    """
    totals = defaultdict(float)
    for rec in expenses:
        cat = rec.get("category", "other")
        totals[cat] += rec.get("amount", 0.0)

    if not totals:
        print("No expense data to plot.")
        return

    labels = list(totals.keys())
    sizes = list(totals.values())

    plt.figure(figsize=(6, 6))
    plt.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Expense Breakdown by Category")
    plt.tight_layout()
    plt.show()


