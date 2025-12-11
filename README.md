# BudgetMaster

BudgetMaster is a small Python package that helps users keep track of
income, expenses and monthly budgets in a simple way. 

The package `budgetmaster` has three sub-packages:

- `income`
- `expense`
- `analysis`

Each sub-package has two modules. One of these two module uses inheritance to
satisfy the DATA 533's project requirements.


## 1. income sub-package

### 1.1 `budgetmaster.income.entry`

This module stores income records in a simple Python list.  
Each income record is a dictionary with the keys:
`income_id`, `source`, `amount`, and `date`.

Functions:

- `add_income(source, amount, date)`

  Creates a new income record and adds it to the list. The `amount`
  must be non-negative (we checked it by using `validate_amount`). The function returns the created record as
  a dictionary.

- `update_income(income_id, new_source=None, new_amount=None, new_date=None)`

  Updates an existing income record with the given `income_id`.
  Only the arguments that are not `None` are changed. If `new_amount`
  is provided, it is checked with `validate_amount` before updating.  
  If the `income_id` is not found, the function raises a `ValueError`.
  

- `delete_income(income_id)`

  Removes the income record with the matching `income_id` from the list.
  If the id does not exist, nothing happens.

- `get_all_incomes()`

  Returns a list of all current income records. This is useful for
  other modules that need to read the data.



### 1.2 `budgetmaster.income.summary`

This module provides basic summary statistics for the income data.
It calls `get_all_incomes()` from the `entry` module.

Functions:

- `total_monthly_income(month)`

  Calculates the total income for a given month. The `month` should have the 
  form `"YYYY-MM"`, for example `"2025-11"`.  
  The function chooses all incomes where the date starts with this month
  and sums their amounts.

- `average_monthly_income()`

  Computes the average monthly income across all months that appear
  in the data. First it groups incomes by month and then takes the
  mean of the monthly totals. If there is no data, it returns `0.0`.

- `income_by_source()`

  Groups incomes by `source`. The result is a dictionary where the keys
  are sources (for example `"salary"` or `"freelance"`) and the values
  are the total amounts from each source.



## 2. expense sub-package

### 2.1 `budgetmaster.expense.base_transaction`

This module defines a base class that will be reused by the `Expense`
class. 

Class:

- `BaseTransaction(amount, date, description="")`

  Attributes:
  - `amount`: a non-negative number
  - `date`: a string, for example `"2025-11-20"`
  - `description`: a short text

  Methods:
  - `update(new_amount=None, new_date=None, new_description=None)`

    Updates the fields of the transaction. Only values that are not
    `None` are changed.

  - `to_dict()`

    Converts the object into a dictionary, which is convenient for
    storing in a list.



### 2.2 `budgetmaster.expense.entry`

This module contains the `Expense` class and helper functions
to work with expense records. Expenses are stored in a list of
dictionaries, similar to incomes. The module also uses
`validate_amount()` from `budgetmaster.analysis.utils` to make
sure expense amounts are non-negative.

Class:

- `Expense(category, amount, date, description="")`

  This class inherits from `BaseTransaction` and adds extra information:

  - `category`: for example `"food"`, `"rent"`, `"entertainment"`
  - `tags`: a list of small labels, stored as a Python list

  Methods:
  - `is_over_budget(category_limit)`: returns `True` if the amount is
    larger than the given limit.
  - `add_tag(tag)`: adds a tag string to the `tags` list.

Functions:

- `add_expense(category, amount, date, description="")`

  Creates an `Expense` object and saves it as a dictionary in a list.
  The returned dictionary includes an `expense_id` that can be used
  to refer to this record later. The `amount` is checked with
  `validate_amount` before the record is stored.

- `get_all_expenses()`

  Returns a list of all stored expense dictionaries.

- `delete_expense(expense_id)`

  Deletes the expense whose `expense_id` matches the input. If the id
  is not found, nothing happens.

- `total_by_category()`

  Computes the total expense for each category and returns a dictionary
  where the keys are categories and the values are the sums.



## 3. analysis sub-package

### 3.1 `budgetmaster.analysis.reports`

This module combines income and expense data to create simple reports.

Functions:

- `monthly_balance(incomes, expenses)`

  Takes a list of income records and a list of expense records.
  It groups them by month and returns a dictionary where each key is
  a month (for example `"2025-12"`) and each value is
  `(total income - total expense)` for that month.

- `savings_rate(incomes_total, expenses_total)`

  Computes the savings rate as  
  `(incomes_total - expenses_total) / incomes_total`.  
  If `incomes_total` is less than or equal to zero, the function
  returns `0.0`.

- `generate_report(balance_data)`

  Takes the output of `monthly_balance` and converts it into a simple
  multiline text report. Each line shows the month, the balance,
  and whether it is a surplus or a deficit.
  
- `plot_monthly_balance(balance_data)`  
  Draws a bar chart showing the net balance for each month.

- `plot_income_vs_expense(incomes, expenses)`  
  Produces a grouped bar chart comparing monthly income and monthly
  expense totals.

- `plot_category_expense(expenses)`  
  Creates a pie chart showing how total expenses are distributed
  across categories.


### 3.2 `budgetmaster.analysis.utils`

This module contains helper functions that are used by other parts of
the package.

Functions:

- `categorize_expense(expense)`

  Tries to guess a category based on the description text in the
  expense dictionary. For example, if the description contains words
  like `"rent"` or `"mortgage"`, the category `"housing"` is returned.
  If a category already exists in the dictionary, the existing value
  is used.

- `format_currency(amount)`

  Formats a number as a simple currency string, for example:
  `1234.5` becomes `"$1234.50"`.

- `validate_amount(amount)`

  Checks that the amount is non-negative. If it is negative, the
  function raises a `ValueError`. This helper is used by both
  `income.entry` and `expense.entry` so the validation logic is shared.


## 4. Installation (PyPI)

The package is officially published on PyPI:

**[https://pypi.org/project/budgetmaster-mds533-ubctao/0.1.0/](https://pypi.org/project/budgetmaster-mds533-ubctao/0.1.0/)**

### Install with:

```bash
pip install budgetmaster-mds533-ubctao
```

### Import example:

```python
import budgetmaster
from budgetmaster.income.entry import add_income
from budgetmaster.expense.entry import add_expense
from budgetmaster.analysis.reports import monthly_balance
```


## 5. Project Structure

```
project-step-3-UBCTAO/
│
├── budgetmaster/
│   ├── income/
│   │   ├── __init__.py
│   │   ├── entry.py
│   │   └── summary.py
│   │
│   ├── expense/
│   │   ├── __init__.py
│   │   ├── base_transaction.py   # Base class (inheritance requirement)
│   │   └── entry.py              # Expense inherits BaseTransaction
│   │
│   └── analysis/
│       ├── __init__.py
│       ├── reports.py
│       └── utils.py
│
├── tests/
│   ├── test_income_entry.py
│   ├── test_income_summary.py
│   ├── test_expense_entry.py
│   ├── test_expense_base_transaction.py
│   ├── test_analysis_utils.py
│   └── test_analysis_reports.py
│
├── pyproject.toml               # required for PyPI packaging
├── README.md
└── .github/workflows/main.yml   # CI workflow
```


## 6. GitHub Actions (CI)

We configured automated testing using GitHub Actions.
Every push or pull request to `main` triggers:

* Setup of Python 3.11
* Installation of dependencies
* Running all unit tests under `tests/`
* Generating coverage report

The CI workflow file is located at:

```
.github/workflows/main.yml
```

### CI status:

* All tests pass successfully
* CI is fully functional
* Meets project requirements



## 7. Test Coverage Summary

We executed:

```bash
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report -m
```

### Results:

* All project modules are tested
* Test coverage meets requirements (≥75%)
* Plotting functions (matplotlib) naturally have lower coverage and are excluded from logic tests
* Coverage report is included in the repository



## 8. Demo Video

**The video is submitted on Canvas as required.**




