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
        lst = [4, 4, 1, 5]
        total_bus = 4
        max_guest = 5
        h.ship(total_bus, lst.copy(), max_guest)

        expected = [2, 5, 9, 14, 4, 8, 13, 9, 7, 11, 17, 24, 32, 41]

        for i in expected:
            self.assertIn('found', h.search(i))

        self.assertEqual('room 1 is empty', h.search(1))

        lst = [100, 1, 1, 1, 150]
        total_bus = 5
        max_guest = 150
        h.ship(total_bus, lst.copy(), max_guest)

        for i, bus in enumerate(lst):
            for j in range(bus):
                tmp = cantor_pair(i + 1, j + 1)
                self.assertIn('found', h.search(tmp))

        # test case where bus more than guests
        lst = [5, 1, 3, 2, 1, 3]
        total_bus = 6
        max_guest = 5
        h.ship(total_bus, lst.copy(), max_guest)

        for i, bus in enumerate(lst):
            for j in range(bus):
                tmp = cantor_pair(i + 1, j + 1)
                self.assertIn('found', h.search(tmp))

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
