import unittest
from budgetmaster.expense import entry as expense_entry


class TestExpenseEntry(unittest.TestCase):
    """Tests for budgetmaster.expense.entry."""

    @classmethod
    def setUpClass(cls):
        print("setUpClass: TestExpenseEntry")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: TestExpenseEntry")

    def setUp(self):
        # reset the in-memory storage and id counter in expense_entry
        if hasattr(expense_entry, "_expenses"):
            expense_entry._expenses.clear()
        if hasattr(expense_entry, "_next_expense_id"):
            expense_entry._next_expense_id = 1
    
    def tearDown(self):
        # clean up after each test as well
        if hasattr(expense_entry, "_expenses"):
            expense_entry._expenses.clear()
        if hasattr(expense_entry, "_next_expense_id"):
            expense_entry._next_expense_id = 1


    def test_add_and_total_by_category_and_is_over_budget(self):
        """test add_expense / total_by_category / is_over_budget。"""
        e1 = expense_entry.add_expense("food", 20.0, "2025-01-01", "lunch")
        e2 = expense_entry.add_expense("rent", 800.0, "2025-01-02", "apartment")
        e3 = expense_entry.add_expense("food", 30.0, "2025-01-03", "dinner")

        self.assertEqual(e1["expense_id"], 1)
        self.assertEqual(e2["category"], "rent")
        self.assertEqual(len(expense_entry.get_all_expenses()), 3)
        totals = expense_entry.total_by_category()
        self.assertEqual(totals["food"], 50.0)
        self.assertEqual(totals["rent"], 800.0)


        exp_obj = expense_entry.Expense("entertainment", 100, "2025-01-05")
        self.assertTrue(exp_obj.is_over_budget(50))
        self.assertFalse(exp_obj.is_over_budget(150))
   
    def test_add_tag_delete_expense_and_validation(self):
        """test add_tag、delete_expense and when amount is nagtive。"""
        e1 = expense_entry.add_expense("entertainment", 60, "2025-01-10", "movie")
        expense_id = e1["expense_id"]

        # test add_tag
        exp_obj = expense_entry.Expense("food", 15, "2025-01-11")
        exp_obj.add_tag("snack")
        exp_obj.add_tag("coffee")
        self.assertIn("snack", exp_obj.tags)
        self.assertEqual(len(exp_obj.tags), 2)
        self.assertEqual(exp_obj.amount, 15)

        # test delete_expense
        expense_entry.delete_expense(expense_id)
        ids = [rec["expense_id"] for rec in expense_entry.get_all_expenses()]
        self.assertNotIn(expense_id, ids)

        # when amount is neagtive 
        with self.assertRaises(ValueError):
            expense_entry.add_expense("food", -5, "2025-01-12", "bad amount")
