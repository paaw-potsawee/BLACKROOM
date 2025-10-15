import sys
import os
import random
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))

from hotel import Hotel  # NOQA


def cantor_pair(bus: int, i: int) -> int:
    return ((bus + i) * (bus + i - 1)) // 2 + i


class TestHotel(unittest.TestCase):
    def setUp(self):
        random.seed(888)

    def test_walk_in_unique(self):
        h = Hotel()
        n = 5000
        h.walk_in(n, profile_msg='initialize')

        for k in range(1, n + 1):
            self.assertIn('found', h.search(
                k), 'initialize should have no empty room')

        h.walk_in(n)
        for k in range(1, n + 1):
            self.assertEqual(f'found: WLK_FIN-{1:03d}-{k:09d}', h.search(
                k), 'walk in room alignment incorrect')

        for k in range(n + 1, 2 * n + 1):
            self.assertEqual(f'found: INT_INF-{0:03d}-{k:09d}', h.search(
                k), 'walk in room alignment incorrect')

    def test_bus_unique(self):
        h = Hotel()
        h.walk_in(1000, profile_msg='initialize')
        total_bus, guest_per_bus = 7, 1500
        h.bus(total_bus, guest_per_bus)
        M = total_bus + 1
        expected = set((i * M) - b for b in range(1, total_bus + 1)
                       for i in range(1, guest_per_bus + 1))

        self.assertEqual(len(expected), total_bus * guest_per_bus)
        sample = random.sample(list(expected), 200)
        for k in sample:
            self.assertIn("found:", h.search(k))

    def test_ship_unique_large(self):
        h = Hotel()
        # Seed with many walk-ins to ensure transform interacts with data
        h.walk_in(20000, profile_msg="initialize")

        bus_per_ship = 100
        guest_per_bus = 500
        # Expected set using the corrected unique pairing
        expected = set(cantor_pair(bus, i) for bus in range(
            1, bus_per_ship + 1) for i in range(1, guest_per_bus + 1))

        self.assertEqual(len(expected), bus_per_ship * guest_per_bus,
                         'formula for ship should have unique key value')

        # verify formula with output from excel
        self.assertEqual(cantor_pair(0, 21), 231,
                         'Calculation ship key should return same value as Excel')

        h.ship(bus_per_ship, guest_per_bus)

        # Verify a broad random sample
        sample = random.sample(list(expected), 500)
        for k in sample:
            self.assertIn("found:", h.search(k))

    def test_manual_insert_can_replace(self):
        h = Hotel()
        h.walk_in(10, profile_msg="initialize")
        before = h.search(5)
        self.assertIn("found:", before)
        h.manual_insert(5)
        after = h.search(5)
        self.assertIn("found:", after)
        self.assertNotEqual(before, after)  # replaced


if __name__ == '__main__':
    unittest.main()
