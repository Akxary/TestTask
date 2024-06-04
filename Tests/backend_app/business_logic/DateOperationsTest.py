import unittest
from datetime import date
from business_logic.date_operations import (
    get_last_day_of_month,
    calculate_retirement_date,
    get_next_payment_date,
    get_previous_payment_date,
    calculate_payment_date_boundaries,
    get_period_number
)


class DateOperationsTest(unittest.TestCase):

    def base_output(self, k, v, ans):
        print(
            f"[{'passed' if v==ans else 'failed'}] for {k=} expected: {v=} actual: {ans=}"
        )
        self.assertEqual(v, ans)

    def test_get_last_day_of_month(self):
        test_map = {
            date(2020, 1, 1): date(2020, 1, 31),
            date(2024, 2, 26): date(2024, 2, 29),
        }
        for k, v in test_map.items():
            ans = get_last_day_of_month(k)
            self.base_output(k, v, ans)

    def test_calculate_retirement_date(self):
        test_map = {
            (date(2020, 1, 1), 10): date(2030, 1, 31),
            (date(2024, 2, 26), 15): date(2039, 2, 28),
        }
        for k, v in test_map.items():
            ans = calculate_retirement_date(k[0], k[1])
            self.base_output(k, v, ans)

    def test_get_next_payment_date(self):
        test_map = {
            date(2020, 1, 31): date(2020, 2, 29),
            date(2024, 3, 31): date(2024, 4, 30),
            date(2023, 12, 31): date(2024, 1, 31),
        }
        for k, v in test_map.items():
            ans = get_next_payment_date(k)
            self.base_output(k, v, ans)

    def test_get_previous_payment_date(self):
        test_map = {
            date(2020, 1, 31): date(2019, 12, 31),
            date(2024, 3, 31): date(2024, 2, 29),
        }
        for k, v in test_map.items():
            ans = get_previous_payment_date(k)
            self.base_output(k, v, ans)

    def test_calculate_payment_date_boundaries(self):
        test_map = {
            (date(2020, 1, 1), 10, 11): (date(2030, 1, 31), date(2031, 1, 31)),
            (date(2024, 2, 26), 15, 17): (date(2039, 2, 28), date(2041, 2, 28)),
        }
        for k, v in test_map.items():
            ans = calculate_payment_date_boundaries(k[0], k[1], k[2])
            # self.assertTupleEqual()
            self.base_output(k, v, ans)

    def test_get_period_number(self):
        test_map = {
            (date(2020, 2, 3), date(2020, 2, 29)): 0,
            (date(2024, 4, 20), date(2024, 2, 29)): 1,
            (date(2023, 12, 31), date(2022, 11, 30)): 13,
        }
        for k, v in test_map.items():
            ans = get_period_number(k[0], k[1])
            self.base_output(k, v, ans)
