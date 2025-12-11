import unittest
from budgetmaster.income import entry as income_entry


class TestIncomeEntry(unittest.TestCase):
    """Tests for budgetmaster.income.entry."""

    @classmethod
    def setUpClass(cls):
        print("setUpClass: TestIncomeEntry")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: TestIncomeEntry")

    def setUp(self):
        income_entry.incomes.clear()
        income_entry.next_income_id = 1

    def tearDown(self):
        income_entry.incomes.clear()
        income_entry.next_income_id = 1

    def test_add_income_creates_records_and_ids(self):
        """add_income should create a record and the id should increment."""
        r1 = income_entry.add_income("salary", 1000, "2025-01-01")
        r2 = income_entry.add_income("freelance", 500, "2025-01-10")

        self.assertEqual(r1["income_id"], 1)
        self.assertEqual(r2["income_id"], 2)
        self.assertEqual(len(income_entry.incomes), 2)
        self.assertAlmostEqual(
            sum(rec["amount"] for rec in income_entry.incomes),
            1500.0,
        )

    def test_update_and_delete_income_and_validation(self):
        """update_income / delete_income and error handling"""
        rec = income_entry.add_income("salary", 1000, "2025-01-01")
        income_id = rec["income_id"]

        updated = income_entry.update_income(
            income_id,
            new_source="bonus",
            new_amount=1200,
            new_date="2025-01-05",
        )

        self.assertEqual(updated["source"], "bonus")
        self.assertEqual(updated["amount"], 1200.0)
        self.assertEqual(updated["date"], "2025-01-05")
        self.assertEqual(len(income_entry.get_all_incomes()), 1)

        income_entry.delete_income(income_id)
        self.assertEqual(len(income_entry.get_all_incomes()), 0)

        # when id doesn't exist
        with self.assertRaises(ValueError):
            income_entry.update_income(999, new_amount=10)

        # when amount is negative 
        with self.assertRaises(ValueError):
            income_entry.add_income("salary", -1, "2025-01-01")
