import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))

from BPlusTree import BPlusTree  # NOQA


class TestAffineBasic(unittest.TestCase):
    def test_offset_insert_search_replace(self):
        t = BPlusTree(order=4)
        t.insert((1, 'A'))
        t.insert((5, 'B'))

        # add 100 to every room number (no materialize needed for exact keys)
        t.process_room_number(lambda x: x + 100)

        self.assertEqual(t.search(101), 'A')
        self.assertEqual(t.search(105), 'B')
        self.assertEqual(t.search(3), -1)

        # insert exact (103 -> stored 3) and then replace it
        t.insert((103, 'C'))
        self.assertEqual(t.search(103), 'C')
        t.insert((103, 'C2'))
        self.assertEqual(t.search(103), 'C2')

    def test_multiply_materialize_on_non_lattice_insert(self):
        t = BPlusTree(order=4)
        test_case = [(1, 'A'), (2, 'B'), (4, 'C')]
        for k, v in test_case:
            t.insert((k, v))

        t.process_room_number(lambda x: 2 * x)
        self.assertEqual(t.search(2), 'A')
        self.assertEqual(t.search(4), 'B')
        self.assertEqual(t.search(8), 'C')

        # Insert 3 (non-lattice under s = 2) triggers materialize then insert
        t.insert((3, 'X'))
        self.assertEqual(t.search(2), 'A')
        self.assertEqual(t.search(4), 'B')
        self.assertEqual(t.search(8), 'C')
        self.assertEqual(t.search(3), 'X')

    def test_delete_under_affine(self):
        t = BPlusTree(order=4)
        for k in range(1, 9):
            t.insert((k, f'G{k}'))

        t.process_room_number(lambda x: 2 * x)

        # Delete an exact lattice key
        self.assertNotEqual(t.delete(4), -1)
        self.assertEqual(t.search(4), -1)

        # Delete a non-lattice key (should be no-op)
        self.assertEqual(t.search(5), -1)
        self.assertEqual(t.search(2), 'G1')
        self.assertEqual(t.search(6), 'G3')


if __name__ == "__main__":
    unittest.main()
