import unittest
from budgetmaster.income import entry as income_entry
from budgetmaster.income import summary as income_summary


class TestIncomeSummary(unittest.TestCase):
    """Tests for budgetmaster.income.summary."""

    @classmethod
    def setUpClass(cls):
        print("setUpClass: TestIncomeSummary")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass: TestIncomeSummary")

    def setUp(self):
        income_entry.incomes.clear()
        income_entry.next_income_id = 1
        income_entry.add_income("salary", 3000, "2025-01-01")
        income_entry.add_income("freelance", 500, "2025-01-15")
        income_entry.add_income("salary", 3200, "2025-02-01")

    def tearDown(self):
        income_entry.incomes.clear()
        income_entry.next_income_id = 1

    def test_total_monthly_income(self):
        total_jan = income_summary.total_monthly_income("2025-01")
        total_feb = income_summary.total_monthly_income("2025-02")
        total_mar = income_summary.total_monthly_income("2025-03")

        self.assertEqual(total_jan, 3500.0)
        self.assertEqual(total_feb, 3200.0)
        self.assertEqual(total_mar, 0.0)
        self.assertLess(total_mar, total_jan)

    def test_average_income_and_by_source(self):
        avg = income_summary.average_monthly_income()
        by_source = income_summary.income_by_source()
        self.assertAlmostEqual(avg, 6700.0 / 2)
        self.assertIn("salary", by_source)
        self.assertEqual(by_source["salary"], 6200.0)
        self.assertEqual(by_source["freelance"], 500.0)
        self.assertEqual(len(by_source.keys()), 2)
