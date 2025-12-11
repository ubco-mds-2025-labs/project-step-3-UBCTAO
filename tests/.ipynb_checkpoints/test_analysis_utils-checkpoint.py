import unittest
from budgetmaster.analysis import utils


class TestAnalysisUtils(unittest.TestCase):
    """Tests for budgetmaster.analysis.utils."""

    @classmethod
    def setUpClass(cls):
        print("setUpClass: TestAnalysisUtils")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: TestAnalysisUtils")

    def setUp(self):
        self.base_expense = {
            "amount": 10.0,
            "date": "2025-01-01",
            "description": "coffee at cafe",
        }

    def tearDown(self):
        self.base_expense = None

    def test_categorize_expense_uses_existing_and_keywords(self):
        """check categorize_expense work with existing categories and keywords."""
        # when a category already exists
        with_category = dict(self.base_expense)
        with_category["category"] = "custom"
        cat1 = utils.categorize_expense(with_category)
        self.assertEqual(cat1, "custom")

        # Judge by the keywords in the description
        rent_exp = {"amount": 800, "date": "2025-01-02", "description": "pay rent"}
        food_exp = {"amount": 20, "date": "2025-01-03", "description": "grocery shopping"}
        trans_exp = {"amount": 5, "date": "2025-01-04", "description": "bus ticket"}
        other_exp = {"amount": 12, "date": "2025-01-05", "description": "random stuff"}

        self.assertEqual(utils.categorize_expense(rent_exp), "housing")
        self.assertEqual(utils.categorize_expense(food_exp), "food")
        self.assertEqual(utils.categorize_expense(trans_exp), "transportation")
        self.assertEqual(utils.categorize_expense(other_exp), "other")

    def test_format_currency_and_validate_amount(self):
        """test format_currency and validate_amount"""
        s1 = utils.format_currency(1234.5)
        s2 = utils.format_currency(0)

        self.assertEqual(s1, "$1234.50")
        self.assertEqual(s2, "$0.00")
        self.assertTrue(s1.startswith("$"))
        self.assertIn(".00", s2)

        # 0 and positive numbers should be passed through validate_amount
        utils.validate_amount(0)
        utils.validate_amount(10.5)

        # when the amount is negative
        with self.assertRaises(ValueError):
            utils.validate_amount(-0.01)
