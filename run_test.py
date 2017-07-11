import unittest
import drug_extraction as de


class TestDrugName(unittest.TestCase):
    def test_drug_extraction(self):
        """Run the tests on function from drug_extraction module."""
        self.assertEqual(de.strict_equal_criteria("hello", "hello"), 1)
        self.assertEqual(de.strict_equal_criteria("hello", "world"), 0)

        self.assertEqual(de.levenshtein_distance("hello", "hello"), 0)
        self.assertEqual(de.levenshtein_distance("examen", "examan"), 1)

    def test(self):
        """Run all the tests of folder."""
        self.test_drug_extraction()


if __name__ == "__main__":
    test_runner = TestDrugName()
    test_runner.test()
