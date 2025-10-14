import os
import sys
import unittest
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from BPlusTree import BPlusTree  # noqa: E402


def tri_var(x: int) -> int:
    # variant used by the tree: x*(x+1)//2
    return x * (x + 1) // 2


class TestBPlusTreeTriangular(unittest.TestCase):
    def setUp(self):
        random.seed(20251012)

    def test_triangular_lookup_small_and_large(self):
        t = BPlusTree(order=64)
        N = 50000
        for i in range(1, N + 1):
            t.insert((i, f"V{i}"))

        # Apply triangular lazily
        t.process_room_number(tri_var)

        # Check sampled points across the range
        for i in [1, 2, 3, 10, 123]:
            self.assertEqual(t.search(tri_var(i)), f"V{i}")

        # Insert a non-image value (5 is not triangular for this variant)
        self.assertEqual(t.search(5), -1)
        t.insert((5, "X"))
        self.assertEqual(t.search(5), "X")
        # Previous triangular values remain correct
        self.assertEqual(t.search(tri_var(1000)), "V1000")

    def test_affine_composition_around_triangular(self):
        t = BPlusTree(order=32)
        for i in range(1, 5000):
            t.insert((i, f"V{i}"))

        C, A, B = 777, 3, 11
        t.process_room_number(lambda x: x + C)                 # affine
        t.process_room_number(lambda x: (x * (x + 1)) // 2)    # triangular
        t.process_room_number(lambda x: A * x + B)             # affine

        for k in [1, 2, 10, 123, 4567]:
            expect = A * tri_var(k + C) + B
            self.assertEqual(t.search(expect), f"V{k}")

        # Non-lattice insert
        new_key = A * tri_var(6000 + C) + B + 1
        t.insert((new_key, "Z"))
        self.assertEqual(t.search(new_key), "Z")


if __name__ == "__main__":
    unittest.main()
