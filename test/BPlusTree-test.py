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
        cls.test_case = [
            (1, 'A'),
            (2, 'B'),
            (3, 'C'),
            (4, 'D'),
            (5, 'E'),
            (6, 'F'),
            (7, 'G'),
            (8, 'H'),
            (9, 'I'),
            (10, 'J'),
            (11, 'K'),
            (12, 'L'),
            (13, 'M'),
            (14, 'N'),
            (15, 'O'),
            (16, 'P'),
            (17, 'Q'),
            (18, 'R'),
            (19, 'S'),
            (20, 'T'),
        ]
        cls.tree = BPlusTree()

    def __is_valid_bplus_tree(self):
        self.__is_valid_leaf_key()
        self.__is_valid_node(self.tree.root, float('-inf'), float('inf'))

    def __is_valid_node(self, node, min_val, max_val):
        self.assertEqual(node.keys, sorted(node.keys),
                         f"Node keys not sored: {node.keys}")

        if not node.is_leaf:
            self.assertEqual(len(node.keys), len(node.children) - 1,
                             f"Internal nod key/child mismatch: {node}")

            for i, child in enumerate(node.children):
                self.assertIsNotNone(child, f"Child pointer is None: {node}")
                self.assertIs(child.parent, node,
                              f"Child's parent pointer is incorrect: {node}")

                child_min = node.keys[i - 1] if i > 0 else min_val
                child_max = node.keys[i] if i < len(node.keys) else max_val
                self.__is_valid_node(child, child_min, child_max)
        else:
            self.assertEqual(len(node.keys), len(node.children),
                             f"Leaf node key/data mismatch: {node}")

    def __is_valid_leaf_key(self):
        node = self.tree.root
        while not node.is_leaf:
            node = node.children[0]
        leaf_keys = []
        while node is not None:
            for i in node.keys:
                leaf_keys.append(i)
            node = node.next_key
        self.assertEqual(leaf_keys, sorted(leaf_keys),
                         f"All leaf key are not sorted")

    def test_insertion(self):
        for case in self.test_case:
            self.tree.insert(case)
            self.__is_valid_bplus_tree()

    def test_deletion(self):
        for case in self.test_case:
            self.tree.insert(case)
        for case in reversed(self.test_case):
            self.tree.delete(case[0])
            self.__is_valid_bplus_tree()


if __name__ == '__main__':
    unittest.main()
