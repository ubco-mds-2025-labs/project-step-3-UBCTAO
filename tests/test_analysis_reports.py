import unittest
from budgetmaster.analysis import reports as analysis_reports


class TestAnalysisReports(unittest.TestCase):
    """Tests for budgetmaster.analysis.reports."""

    @classmethod
    def setUpClass(cls):
        print("setUpClass: TestAnalysisReports")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: TestAnalysisReports")

    def setUp(self):
        self.incomes = [
            {"amount": 3000.0, "date": "2025-01-01"},
            {"amount": 3200.0, "date": "2025-02-01"},
        ]
        self.expenses = [
            {"amount": 1500.0, "date": "2025-01-10"},
            {"amount": 1000.0, "date": "2025-02-15"},
        ]

    def tearDown(self):
        self.incomes = []
        self.expenses = []

    def test_monthly_balance(self):
        balance = analysis_reports.monthly_balance(self.incomes, self.expenses)

        self.assertIn("2025-01", balance)
        self.assertIn("2025-02", balance)
        self.assertEqual(balance["2025-01"], 1500.0)
        self.assertEqual(balance["2025-02"], 2200.0)
        self.assertGreater(balance["2025-02"], balance["2025-01"])

    def test_savings_rate_and_generate_report(self):
        income_total = sum(rec["amount"] for rec in self.incomes)
        expense_total = sum(rec["amount"] for rec in self.expenses)

        rate = analysis_reports.savings_rate(income_total, expense_total)
        self.assertGreater(rate, 0.0)
        self.assertLess(rate, 1.0)
        self.assertAlmostEqual(
            rate,
            (income_total - expense_total) / income_total,
        )

        report = analysis_reports.generate_report(
            {"2025-01": 1500.0, "2025-02": 2200.0}
        )
        self.assertIsInstance(report, str)
        self.assertIn("BudgetMaster Monthly Balance Report", report)
        self.assertIn("2025-01", report)
        self.assertIn("2025-02", report)
        self.assertIn("surplus", report)


    def test_plot_functions_run_without_error(self):
        """Make sure plot functions can run without raising errors."""
        balance = {"2025-01": 1500.0, "2025-02": 2200.0}
        analysis_reports.plot_monthly_balance(balance)
        analysis_reports.plot_income_vs_expense(self.incomes, self.expenses)
        expenses_with_cat = [
            {"amount": 1500.0, "date": "2025-01-10", "category": "housing"},
            {"amount": 1000.0, "date": "2025-02-15", "category": "food"},
        ]
        analysis_reports.plot_category_expense(expenses_with_cat)
        self.assertTrue(True)

