import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))

from BPlusTree import BPlusTree  # NOQA


def leftmost_key(node):
    while not node.is_leaf:
        node = node.children[0]
    return node.keys[0] if len(node.keys) > 0 else None


def check_invariants(tree: BPlusTree):
    # materialize to identity for simpler checks on stored domain
    tree._BPlusTree__materialize()

    def dfs(node):
        if node.is_leaf:
            return
        # B+ invariant: len(keys) == len(children) - 1
        assert len(node.keys) == len(node.children) - 1
        # Parent pointers and separator correctness
        for i, child in enumerate(node.children):
            assert child.parent is node
            if i > 0:
                assert node.keys[i - 1] == leftmost_key(child)
        for child in node.children:
            dfs(child)

    dfs(tree.root)

    # Leaf linkage is increasing
    leaf = tree.get_leftmost_node()
    last = None
    while leaf is not None:
        for k in leaf.keys:
            if last is not None:
                assert last < k
            last = k
        leaf = leaf.next_key


class TestDeleteMergeInvariants(unittest.TestCase):
    def test_splits_merges_and_invariants(self):
        t = BPlusTree(order=4)
        # Many inserts to force multi-level splits
        for i in range(1, 101):
            t.insert((i, f'V{i}'))

        # Compose affines; second one (3x+2) after (+5) => scale=3, offset=7
        t.process_room_number(lambda x: x + 5)
        t.process_room_number(lambda x: 3 * x + 2)

        # i = 4 transform -> 19 is exact, 20 is non-exact
        t.insert((20, 'E20'))
        t.insert((19, 'E19'))  # triggers materialize

        # Deletions to cause underflow/borrows/merges
        for k in list(range(10, 18)) + [1, 2, 3, 4, 5]:
            t.delete(k)

        # Invariant check
        check_invariants(t)

        # Spot checks
        self.assertEqual(t.search(35), 'V6')
        self.assertEqual(t.search(20), 'E20')
        self.assertEqual(t.search(19), 'E19')
        self.assertEqual(t.search(15), -1)  # deleted


if __name__ == '__main__':
    unittest.main()
