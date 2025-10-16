import sys
import os
import random
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))

from hotel import Hotel  # NOQA


def cantor_pair(bus: int, i: int) -> int:
    return ((bus + i) * (bus + i - 1)) // 2 + i


def bus_cal(guest, bus, total_bus):
    return ((guest * (total_bus + 1)) - bus)


class TestHotel(unittest.TestCase):
    def setUp(self):
        random.seed(888)

    def test_walk_in_unique(self):
        h = Hotel()
        n = 50
        h.walk_in(n, profile_msg='initialize')

        for k in range(1, n + 1):
            self.assertIn('found', h.search(
                k), 'initialize should have no empty room')

        h.walk_in(n)
        for k in range(1, n + 1):
            self.assertEqual(f'found: WLK_FIN-{1:03d}-{k:05d}-{0:05d}-{k:09d}', h.search(
                k), 'walk in room alignment incorrect')

        for k in range(n + 1, 2 * n + 1):
            self.assertEqual(f'found: INT_INF-{0:03d}-{(0):05d}-{0:05d}-{k:09d}', h.search(
                k), 'walk in room alignment incorrect')

    def test_bus_unique(self):
        h = Hotel()
        n = 10
        h.walk_in(n, profile_msg='initialize')
        total_bus = 4
        lst = [4, 3, 1, 5]
        h.bus(total_bus, lst.copy(), 5, profile_msg='bus (finite) logic')
        # check initial guest shift
        for i in range(1, 10):
            room_num = bus_cal(i, 0, total_bus)
            self.assertIn('found: INT_INF-000', h.search(room_num))

        # check expected output for each bus
        for bus_num, bus in enumerate(lst):
            for i in range(1, bus + 1):
                room_num = bus_cal(i, bus_num + 1, total_bus)
                self.assertIn('found:', h.search(room_num))

        # test in differ dimension
        lst = [1, 2, 3, 1, 2]
        total_bus = len(lst)
        h.bus(total_bus, lst.copy(), 3, profile_msg='bus (finite) logic')

        for bus_num, bus in enumerate(lst):
            for i in range(1, bus + 1):
                room_num = bus_cal(i, bus_num + 1, total_bus)
                self.assertIn('found:', h.search(room_num))

        # tset in exact dimension
        lst = [3] * 4
        total_bus = len(lst)
        h.bus(total_bus, lst.copy(), 3, profile_msg='bus (finite) logic')

        for bus_num, bus in enumerate(lst):
            for i in range(1, bus + 1):
                room_num = bus_cal(i, bus_num + 1, total_bus)
                self.assertIn('found:', h.search(room_num))

    def test_ship_unique(self):
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
        self.assertEqual(before, h.search(5))


if __name__ == '__main__':
    unittest.main()
