# This file collects all the test classes for project step 2 into one test suite.
import unittest

from tests_project_step2.test_income_entry import TestIncomeEntry
from tests_project_step2.test_income_summary import TestIncomeSummary
from tests_project_step2.test_expense_entry import TestExpenseEntry
from tests_project_step2.test_analysis_reports import TestAnalysisReports
from tests_project_step2.test_expense_base_transaction import TestBaseTransaction
from tests_project_step2.test_analysis_utils import TestAnalysisUtils


def suite():
    """Collect all test classes into one suite."""
    test_suite = unittest.TestSuite()

    # add each TestCase class to the suite.
    for case_cls in [
        TestIncomeEntry,
        TestIncomeSummary,
        TestExpenseEntry,
        TestAnalysisReports,
        TestBaseTransaction,
        TestAnalysisUtils,
    ]:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(case_cls)
        test_suite.addTests(tests)

    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
