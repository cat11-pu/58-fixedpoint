import unittest

from fixedpoint import Fixed
from moneyapi import Amount


class TestFixed(unittest.TestCase):
    def test_set_float(self):
        self.assertEqual(Fixed().set(1.5)["value"], 1.5)

    def test_add_values(self):
        left = Fixed()
        left.set(1.0)
        right = Fixed()
        right.set(2.0)
        self.assertEqual(left.add(right).value, 3.0)

    def test_mul_values(self):
        left = Fixed()
        left.set(2.0)
        right = Fixed()
        right.set(0.5)
        self.assertEqual(left.mul(right).value, 1.0)

    def test_stats_shape(self):
        self.assertIn("decimals", Fixed().stats())

    def test_amount_wraps_fixed(self):
        amount = Amount()
        amount.set(1)
        self.assertEqual(amount.fixed.stats()["decimals"], 2)


if __name__ == "__main__":
    unittest.main()
