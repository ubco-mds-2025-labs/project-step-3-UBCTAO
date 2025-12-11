import unittest
from budgetmaster.expense import base_transaction


class TestBaseTransaction(unittest.TestCase):
    """Tests for budgetmaster.expense.base_transaction."""

    @classmethod
    def setUpClass(cls):
        print("setUpClass: TestBaseTransaction")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: TestBaseTransaction")

    def setUp(self):
        self.tran = base_transaction.BaseTransaction(
            amount=100.0,
            date="2025-01-01",
            description="initial",
        )

    def tearDown(self):
        self.tran = None

    def test_init_and_to_dict(self):
        """test __init__ and to_dict 。"""
        d = self.tran.to_dict()

        self.assertEqual(self.tran.amount, 100.0)
        self.assertEqual(self.tran.date, "2025-01-01")
        self.assertEqual(self.tran.description, "initial")
        self.assertEqual(d["amount"], 100.0)
        self.assertIn("date", d)
        self.assertIn("description", d)

        # when amount is negative 
        with self.assertRaises(ValueError):
            base_transaction.BaseTransaction(-1, "2025-01-02", "bad")

    def test_update_fields_and_validation(self):
        """update should correctly update the fields and check for negative amounts."""
        self.tran.update(
            new_amount=150.0,
            new_date="2025-01-10",
            new_description="updated",
        )

        self.assertEqual(self.tran.amount, 150.0)
        self.assertEqual(self.tran.date, "2025-01-10")
        self.assertEqual(self.tran.description, "updated")

        # only update the date, other fields will remain unchanged
        self.tran.update(new_date="2025-01-20")
        self.assertEqual(self.tran.amount, 150.0)
        self.assertEqual(self.tran.date, "2025-01-20")

        # negative amounts should also raise an error in update
        with self.assertRaises(ValueError):
            self.tran.update(new_amount=-5)
