import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))

import unittest  # NOQA
from BPlusTree import BPlusTree  # NOQA


class TestBPlusTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # List of test cases
        cls.test_cases = [
            [13, 2, 3, 12, 4, 7, 9, 11, 1, 10],
            [5, 3, 8, 1, 7, 2, 6, 4],
            [20, 15, 25, 10, 30, 5, 35, 1]
        ]
        cls.trees = []
        cls.sorted_cases = []
        for case in cls.test_cases:
            tree = BPlusTree(order=4)
            for val in case:
                tree.insert(val)
            cls.trees.append(tree)
            cls.sorted_cases.append(sorted(case))

    def test_search_leaf(self):
        for idx, tree in enumerate(self.trees):
            with self.subTest(test_case=idx):
                # Find the leftmost leaf
                node = tree.root
                while not node.is_leaf:
                    node = node.children[0]
                # Check that the smallest value is in the leftmost leaf
                self.assertIn(self.sorted_cases[idx][0], node.keys)

    def test_all_leaves_content(self):
        for idx, tree in enumerate(self.trees):
            with self.subTest(test_case=idx):
                # Collect all values from all leaves
                node = tree.root
                while not node.is_leaf:
                    node = node.children[0]
                result = []
                while node:
                    result.extend(node.keys)
                    node = node.next_key
                self.assertEqual(result, self.sorted_cases[idx])


if __name__ == '__main__':
    unittest.main()
