import sys
import os
import random
from array import array
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))

from BPlusTree import BPlusTree  # NOQA


class TestBPlusTree(unittest.TestCase):
    ORDERS = [3, 4, 8, 16]

    def setUp(self):
        random.seed(8888)

    # Invariant checks

    def _collect_leaves(self, tree: BPlusTree):
        node = tree.root
        depth = 0
        while not node.is_leaf:
            node = node.children[0]
            depth += 1

        seend_ids = set()
        leaves = []
        while node is not None:
            nid = id(node)
            # check for circular linked in leaf node
            self.assertNotIn(nid, seend_ids, "Leaf next_key forms a cycle")
            seend_ids.add(nid)
            leaves.append(node)
            node = node.next_key

        return leaves, depth

    def _leftmost_key(self, node):
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0] if node.keys else None

    def _check_tree(self, tree: BPlusTree):
        self.assertIsNotNone(tree.root)
        leaves, left_depth = self._collect_leaves(tree)
        last_key = None
        all_keys = []
        for leaf in leaves:
            # Leaf keys/children length match and array type kept
            self.assertIsInstance(
                leaf.keys, array, 'Leaf keys must be array(\'i\')')
            self.assertEqual(len(leaf.keys), len(
                leaf.children), 'Leaf key/data mismatch')
            for k in leaf.keys:
                all_keys.append(k)
                if last_key is not None:
                    # test order in of key in leaf node
                    self.assertLess(
                        last_key, k, 'Leaf keys must be strictly increasing across chain')
                last_key = k

        order = getattr(tree, "_BPlusTree_order", None)
        min_leaf = getattr(tree, "_BPlusTree_min_leaf_keys", None)
        min_internal = getattr(tree, "_BPlusTree_min_internal_keys", None)
        max_keys = order - 1 if order is not None else None

        def dfs(node, depth, is_root):
            self.assertEqual(list(node.keys), sorted(
                node.keys), 'Node keys not sorted')
            if node.is_leaf:
                self.assertEqual(depth, left_depth,
                                 'All leaves must be at same depth')
                if not is_root and min_leaf is not None and max_keys is not None:
                    self.assertGreaterEqual(
                        len(node.keys), min_leaf, 'Leaf underflow')
                    self.assertLessEqual(
                        len(node.keys), max_keys, 'Leaf overflow')
                return

            self.assertEqual(len(node.keys), len(
                node.children) - 1, 'Internal key/child mismatch')
            if not is_root and min_internal is not None and max_keys is not None:
                self.assertGreaterEqual(
                    len(node.keys), min_internal, 'Internal underflow')
                self.assertLessEqual(
                    len(node.keys), max_keys, 'Internal overflow')

            for i, child in enumerate(node.children):
                self.assertIs(child.parent, node,
                              'Child.parent pointer is incorrect')
                if i > 0:
                    sep = node.keys[i - 1]
                    lm = self._leftmost_key(child)
                    self.assertEqual(
                        sep, lm, 'Separator must equal left most key of right child')

            for child in node.children:
                dfs(child, depth + 1, is_root=False)

        dfs(tree.root, depth=0, is_root=True)

        def inorder_collect(n):
            if n.is_leaf:
                return list(n.keys)
            out = []
            for c in n.children:
                out.extend(inorder_collect(c))
            return out

        self.assertEqual(all_keys, inorder_collect(
            tree.root), 'In-order traversal mismatch')
        self.assertEqual(len(all_keys), len(
            set(all_keys)), 'Duplicate keys present')

    def test_insert_then_delete_validity(self):
        data = [(i, f"V{i}") for i in range(1, 101)]

        for order in self.ORDERS:
            with self.subTest(order=order):
                t = BPlusTree(order=order)
                oracle = {}

                ins = data.copy()
                random.shuffle(ins)
                for k, v in ins:
                    t.insert((k, v))
                    oracle[k] = v
                    self._check_tree(t)
                    self.assertEqual(t.search(k), v)
                    self.assertEqual(t.search(-k), -1)

                dels = ins.copy()
                random.shuffle(dels)
                for k, _ in dels:
                    t.delete(k)
                    oracle.pop(k, None)
                    self._check_tree(t)
                    self.assertEqual(t.search(k), -1)
                self.assertTrue(
                    t.root.is_leaf, "Root should be leaf after all deletions")
                self.assertEqual(len(t.root.keys), 0,
                                 "Root should have no keys after all deletions")

    def test_replace_existing_key(self):
        for order in self.ORDERS:
            with self.subTest(order=order):
                t = BPlusTree(order=order)
                t.insert((10, "A"))
                self._check_tree(t)
                self.assertEqual(t.search(10), "A")
                # Replace
                t.insert((10, "B"))
                self._check_tree(t)
                self.assertEqual(t.search(10), "B")

    def test_delete_nonexistent_is_noop(self):
        for order in self.ORDERS:
            with self.subTest(order=order):
                t = BPlusTree(order=order)
                for k in [1, 2, 3, 4, 5]:
                    t.insert((k, f"V{k}"))
                self._check_tree(t)
                # Nonexistent deletions
                for k in [0, -1, 6, 100]:
                    res = t.delete(k)
                    self._check_tree(t)


if __name__ == '__main__':
    unittest.main()
