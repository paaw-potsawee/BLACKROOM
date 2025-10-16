from typing import Optional, Any
from array import array
import csv
from math import isqrt


class Node:
    __slots__ = ('__keys', '__children', '__next_key', '__parent', '__is_leaf')

    def __init__(self, is_leaf: bool = True):
        self.__keys: array = array('q')
        self.__children: list[Any] = []
        self.__next_key: Optional["Node"] = None
        self.__parent: Optional["Node"] = None
        self.__is_leaf: bool = is_leaf

    def insert(self, key, val=None):
        n = len(self.__keys)
        if n > 0:
            if key < self.__keys[0]:
                self.__keys.insert(0, key)
                if self.__is_leaf:
                    self.__children.insert(0, val)
                return
            right = n - 1
            left = 0
            if self.__keys[right] < key:
                self.__keys.append(key)
                if self.__is_leaf:
                    self.__children.append(val)
                return
            while left < right:
                mid = left + (right - left) // 2
                if self.__keys[mid] < key:
                    left = mid + 1
                else:
                    right = mid
            self.__keys.insert(left, key)
            if self.__is_leaf:
                self.__children.insert(left, val)
        else:
            self.__keys.append(key)
            if self.__is_leaf:
                self.__children.append(val)

    def __str__(self):
        return f'{list(self.__keys)}'

    @property
    def children(self): return self.__children
    @children.setter
    def children(self, data: list): self.__children = data

    @property
    def keys(self) -> array: return self.__keys

    @keys.setter
    def keys(self, data):
        if isinstance(data, array):
            self.__keys = data
        else:
            self.__keys = array('q', data)

    @property
    def parent(self): return self.__parent
    @parent.setter
    def parent(self, data): self.__parent = data

    @property
    def is_leaf(self): return self.__is_leaf

    @property
    def next_key(self): return self.__next_key
    @next_key.setter
    def next_key(self, data): self.__next_key = data

    def append_key(self, data): self.__keys.append(data)

    def append_child(self, data): self.__children.append(data)

    def insert_key(self, data, i): self.__keys.insert(i, data)

    def get_key_len(self): return len(self.__keys)

    def get_siblings(self, child):
        left, right = None, None
        idx = self.__children.index(child)
        if idx - 1 >= 0:
            left = self.__children[idx - 1]
        if idx + 1 < len(self.__children):
            right = self.__children[idx + 1]
        return left, right, idx

    def is_first_child(self, child):
        if len(self.__children) == 0:
            raise Exception(f'is_fisrt_child should not be called')
        return self.__children[0] is child


class BPlusTree:
    __slots__ = ('__order', '__min_leaf_keys', '__min_internal_keys',
                 '__root', '__g_offset', '__g_scale', '__tri_active', '__in_scale', '__out_scale', '__in_offset', '__out_offset')

    def __init__(self, order: int = 4):
        if order < 3:
            raise ValueError('B+ tree order should not  less than 3')
        self.__order: int = order
        # Leaf min keys = ceil((m-1)/2) == floor(m/2); Internal min keys = ceil(m/2) - 1 == floor((m-1)/2)
        self.__min_leaf_keys: int = self.__order // 2
        self.__min_internal_keys: int = (self.__order - 1) // 2
        self.__root: Node = Node(is_leaf=True)
        self.__g_scale: int = 1
        self.__g_offset: int = 0
        # tri-affine
        self.__tri_active: bool = False
        self.__in_scale: int = 1
        self.__in_offset: int = 0
        self.__out_scale: int = 1
        self.__out_offset: int = 0

    @property
    def root(self): return self.__root

    def insert(self, data):
        self._insert(self.__root, data[0], data[1])

    def _insert(self, node: Node, key, val=None):
        # search for leaf node
        leaf_node = self.search_leaf(node, key)

        phy_key = self.__physical_exact_key(key)
        if phy_key is None:
            # Non-exact under current lazy transform: materialize and insert as-is
            self.__materialize()
            leaf_node = self.search_leaf(self.__root, key)
            phy_key = key

        pos = self.__binary_search(leaf_node.keys, key)
        idx = pos - 1
        if 0 <= idx < len(leaf_node.keys) and phy_key == leaf_node.keys[idx]:
            print(f'Guest exists in room {key}. Can not insert')
            return

        leaf_node.insert(phy_key, val)

        if len(leaf_node.keys) > self.__order - 1:
            mid = len(leaf_node.keys) // 2
            new_leaf = Node(is_leaf=True)
            # Use array slicing to avoid intermediate list allocations.
            new_leaf.keys = leaf_node.keys[mid:]
            leaf_node.keys = leaf_node.keys[:mid]
            # split guest data
            if leaf_node.is_leaf and len(leaf_node.children) > 0:
                new_leaf.children = leaf_node.children[mid:]
                leaf_node.children = leaf_node.children[:mid]

            new_leaf.next_key = leaf_node.next_key
            leaf_node.next_key = new_leaf

            # case where leaf node is root
            if leaf_node.parent is None:
                new_root = Node(is_leaf=False)
                new_root.keys = [new_leaf.keys[0]]
                new_root.children = [leaf_node, new_leaf]
                leaf_node.parent = new_root
                new_leaf.parent = new_root
                self.__root = new_root
            # case where leaf node has parent (continue to check recursively)
            else:
                self._insert_separator(
                    leaf_node.parent, new_leaf.keys[0], new_leaf)

    def _insert_separator(self, parent: Node, val, new_child: Node):
        # insert value and new child to parent
        i = 0
        while i < len(parent.keys) and val > parent.keys[i]:
            i += 1
        parent.keys.insert(i, val)
        parent.children.insert(i + 1, new_child)
        new_child.parent = parent

        # check if parent overflows (if split recursively)
        if len(parent.keys) > self.__order - 1:
            mid = len(parent.keys) // 2
            promoted_val = parent.keys[mid]

            # create new internal node
            new_node = Node(is_leaf=False)
            # Use array slicing here as well to save allocations.
            new_node.keys = parent.keys[mid + 1:]
            new_node.children = parent.children[mid + 1:]
            # point child to new parent
            for child in new_node.children:
                child.parent = new_node

            parent.keys = parent.keys[:mid]
            parent.children = parent.children[:mid + 1]

            if parent.parent is None:
                # root
                new_root = Node(is_leaf=False)
                new_root.keys = [promoted_val]
                new_root.children = [parent, new_node]
                parent.parent = new_root
                new_node.parent = new_root
                self.__root = new_root
            else:
                self._insert_separator(parent.parent, promoted_val, new_node)

    def delete(self, val):
        phy_key = self.__physical_exact_key(val)
        if phy_key is None:
            return -1
        leaf_node = self.search_leaf(self.__root, val)
        try:
            idx = leaf_node.keys.index(phy_key)
        except ValueError:
            return -1

        leaf_node.keys.remove(phy_key)
        if leaf_node.is_leaf:
            leaf_node.children.pop(idx)

        parent = leaf_node.parent
        # if leaf node is root
        if parent is None:
            return

        # if leaf node has at least min_key
        if leaf_node.get_key_len() >= self.__min_leaf_keys:
            # if first value of keys update separator recursively
            self.__update_separator(leaf_node)
            return

        # underflow
        left, right, leaf_idx = parent.get_siblings(leaf_node)
        # try from left first
        if left and left.get_key_len() > self.__min_leaf_keys:
            leaf_node.keys.insert(0, left.keys.pop())
            if left.is_leaf and len(left.children) > 0:
                leaf_node.children.insert(0, left.children.pop())
            self.__update_separator(leaf_node)
            return
        # try from right if left failed
        if right and right.get_key_len() > self.__min_leaf_keys:
            leaf_node.keys.append(right.keys.pop(0))
            if right.is_leaf and len(right.children) > 0:
                leaf_node.children.append(right.children.pop(0))
            self.__update_separator(right)
            self.__update_separator(leaf_node)
            return

        # merge with sibling try merge with left (if exists) then with right
        if left:
            # merge with left node
            self.__merge_node(left, leaf_node, parent, leaf_idx - 1)
            if len(parent.keys) < self.__min_internal_keys:
                self.__handle_internal_underflow(parent)
            self.__update_separator(left)
            return
        elif right:
            # merge with right node
            self.__merge_node(leaf_node, right, parent, leaf_idx)
            self.__handle_internal_underflow(parent)
            self.__update_separator(leaf_node)
            return

    def __merge_node(self, left: Node, right: Node, parent: Node, separator_idx):
        if left is None or right is None:
            return
        if left.is_leaf and right.is_leaf:
            # ensure consistencies while develop
            assert len(left.keys) == len(left.children)
            assert len(right.keys) == len(right.children)
            # merge two leaves
            left.keys.extend(right.keys)
            left.children.extend(right.children)

            left.next_key = right.next_key
        else:
            # merge two internals: move children and rebuild keys from children
            left.children.extend(right.children)
            for child in right.children:
                child.parent = left
            self.__rebuild_internal_keys(left)

        # always remove the separator key at separator_idx
        parent.keys.pop(separator_idx)
        parent.children.remove(right)

    def __handle_internal_underflow(self, node: Node):
        parent = node.parent
        if parent is None:
            if len(node.children) == 1:
                self.__root = node.children[0]
                self.__root.parent = None
            return

        left, right, idx = parent.get_siblings(node)

        # borrow from left
        if left and len(left.keys) > self.__min_internal_keys:
            # move last child from left into node (front)
            child = left.children.pop()
            node.children.insert(0, child)
            child.parent = node
            # rebuild keys for both internals and update the separator in parent
            self.__rebuild_internal_keys(left)
            self.__rebuild_internal_keys(node)
            parent.keys[idx - 1] = self.__leftmost_key(node)
            return

        # borrow from right
        if right and len(right.keys) > self.__min_internal_keys:
            # move first child from right into node (end)
            child = right.children.pop(0)
            node.children.append(child)
            child.parent = node
            # rebuild keys for both internals and update the separator in parent
            self.__rebuild_internal_keys(right)
            self.__rebuild_internal_keys(node)
            parent.keys[idx] = self.__leftmost_key(right)
            return

        # merge with left
        if left:
            self.__merge_node(left, node, parent, idx - 1)
            if len(parent.keys) < self.__min_internal_keys:
                self.__handle_internal_underflow(parent)
            return

        # merge with right
        if right:
            self.__merge_node(node, right, parent, idx)
            if len(parent.keys) < self.__min_internal_keys:
                self.__handle_internal_underflow(parent)
            return

    def __rebuild_internal_keys(self, node: Node):
        # Rebuild internal node keys so that keys[i] == leftmost_key(children[i+1])
        if node.is_leaf:
            return
        new_keys = array('q')
        for i in range(len(node.children) - 1):
            new_keys.append(self.__leftmost_key(node.children[i + 1]))
        node.keys = new_keys

    def __update_separator(self, node: Node):
        # Update only the necessary separator (the one immediately before 'node')
        # while walking up to the root, instead of recomputing all separators.
        parent = node.parent
        while parent is not None:
            try:
                idx = parent.children.index(node)
            except ValueError:
                break
            if idx > 0:
                parent.keys[idx -
                            1] = self.__leftmost_key(parent.children[idx])
            node = parent
            parent = parent.parent

    def __leftmost_key(self, node: Node):
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0]

    def process_room_number(self, cal_func):
        """
        Accept only:
         - affine: f(x) = a*x + b, a > 0
         - triangular: f(x) = x*(x+1)//2
         Any other function is rejected (raise Value error)
        """
        y0 = int(cal_func(0))
        y1 = int(cal_func(1))
        y2 = int(cal_func(2))
        y3 = int(cal_func(3))
        if (y0, y1, y2, y3) == (0, 1, 3, 6):
            self.__compose_triangular()
            return

        d1 = y1 - y0
        if (y2 - y1) == d1 and (y3 - y2) == d1:
            self.__compose_affine(int(d1), int(y0))
            return

        raise ValueError('function is not acceptable by process_room_number')

    def search_leaf(self, node: Node, val):
        while not node.is_leaf:
            child_idx = self.__binary_search(node.keys, val)
            node = node.children[child_idx]
        return node

    def __binary_search(self, keys: array, val: int) -> int:
        """
        Return the index of the first key (strictly) greater than the given logical value.
        """
        phs_val = self.__physical_key(val)
        left, right = 0, len(keys)
        while left < right:
            mid = left + (right - left) // 2
            if keys[mid] <= phs_val:
                left = mid + 1
            else:
                right = mid
        return left

    def __compose_affine(self, a: int, b: int):
        if a <= 0:
            raise ValueError("Affine scale must be positive")

        if self.__tri_active:
            self.__out_scale = a * self.__out_scale
            self.__out_offset = a * self.__out_offset + b
            return
        self.__g_scale = a * self.__g_scale
        self.__g_offset = a * self.__g_offset + b

    def __compose_triangular(self):
        if self.__tri_active:
            self.__materialize()

        self.__in_scale = self.__g_scale
        self.__in_offset = self.__g_offset
        self.__out_scale = 1
        self.__out_offset = 0
        self.__tri_active = True
        self.__g_scale = 1
        self.__g_offset = 0

    def __logical_key(self, stored_key: int):
        if not self.__tri_active:
            return self.__g_scale * stored_key + self.__g_offset
        n = self.__in_scale * stored_key + self.__in_offset
        return self.__out_scale * (n*(n + 1) // 2) + self.__out_offset

    def __physical_key(self, logical_key: int):
        if not self.__tri_active:
            return (logical_key - self.__g_offset) // self.__g_scale
        u = (logical_key - self.__out_offset) // self.__out_scale
        r = isqrt(8 * u + 1)
        n_floor = (r - 1) // 2
        return (n_floor - self.__in_offset) // self.__in_scale

    def __physical_exact_key(self, logical_key: int):
        if not self.__tri_active:
            d = logical_key - self.__g_offset
            return d // self.__g_scale if d % self.__g_scale == 0 else None
        d2 = logical_key - self.__out_offset
        if d2 % self.__out_scale != 0:
            return None
        u = d2 // self.__out_scale
        r = isqrt(8 * u + 1)
        if r * r != 8 * u + 1:
            return None
        n = (r - 1) // 2
        if n * (n + 1) // 2 != u:
            return None
        d1 = n - self.__in_offset
        if d1 % self.__in_scale != 0:
            return None
        return d1 // self.__in_scale

    def __materialize(self):
        # if no scale and offset nothing to change
        if (not self.__tri_active) and self.__g_scale == 1 and self.__g_offset == 0:
            return

        stack = [self.__root]

        while stack:
            node = stack.pop()
            # apply current affine to every key (stored(physical) -> logical), preserving order
            node.keys = array('q', (self.__logical_key(k) for k in node.keys))

            if not node.is_leaf:
                stack.extend(node.children)

        # reset all scale and offset
        self.__g_scale = 1
        self.__g_offset = 0
        self.__tri_active = False
        self.__in_scale = 1
        self.__in_offset = 0
        self.__out_scale = 1
        self.__out_offset = 0

    def get_leftmost_node(self):
        node = self.__root
        while not node.is_leaf:
            node = node.children[0]

        return node

    def search(self, val: int):
        k_exact = self.__physical_exact_key(val)
        if k_exact is None:
            return -1
        leaf = self.search_leaf(self.__root, val)
        pos = self.__binary_search(leaf.keys, val)
        idx = pos - 1
        if 0 <= idx < len(leaf.keys) and leaf.keys[idx] == k_exact:
            return leaf.children[idx]
        return -1

    def print_tree(self):
        print('print entire tree')
        self._print_tree(self.__root, 0)

    def _print_tree(self, node: Node, level: int):
        if node is not None:
            print(
                f'{level} -> {node}')
            if not node.is_leaf:
                for child in node.children:
                    self._print_tree(child, level + 1)

    def print_leaf(self):
        if self.is_empty():
            print('Hotel empty')
            return
        node = self.__root
        while not node.is_leaf:
            node = node.children[0]
        self._print_leaf(node, 1)

    def _print_leaf(self, node: Optional[Node], count):
        while node is not None:
            for i in range(len(node.keys)):
                logical_key = self.__logical_key(node.keys[i])
                print(
                    f'{count: >9d}: {node.children[i]}-{logical_key:09d}', end='\n')
                count += 1
            node = node.next_key
        print('')

    def export_to_csv(self, filename: str = "hotel.csv"):
        node = self.__root
        while not node.is_leaf:
            node = node.children[0]

        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["No", "Method-group_order-order-bus_order-Room_Number"])

            while node is not None:
                for i in range(len(node.keys)):
                    key = self.__logical_key(node.keys[i])
                    value = f'{node.children[i]}-{key:09d}'
                    writer.writerow([key, value])
                node = node.next_key

        print(f"Guest data exported to {filename}")

    def is_empty(self) -> bool:
        # Fast check for an empty tree (single empty leaf).
        return self.__root.is_leaf and len(self.__root.keys) == 0

    def bulk_load(self, sorted_pairs: list[tuple[int, Any]]):
        # Build a B+ tree from sorted (key, value) pairs in linear time.
        if not sorted_pairs:
            # Reset to an empty leaf root
            self.__root = Node(is_leaf=True)
            return

        if self.__tri_active or self.__g_offset != 0 or self.__g_scale != 1:
            self.__materialize()

        # max keys per node (leaf/internal)
        max_keys = self.__order - 1
        max_children = self.__order  # max children per internal

        # Build leaves
        leaves: list[Node] = []
        n = len(sorted_pairs)
        i = 0
        prev_leaf = None
        while i < n:
            chunk = sorted_pairs[i:i + max_keys]
            keys_chunk = array('q', (k for k, _ in chunk))
            vals_chunk = [v for _, v in chunk]

            leaf = Node(is_leaf=True)
            leaf.keys = keys_chunk
            leaf.children = vals_chunk

            if prev_leaf is not None:
                prev_leaf.next_key = leaf
            prev_leaf = leaf
            leaves.append(leaf)
            i += max_keys

        if len(leaves) == 1:
            self.__root = leaves[0]
            self.__root.parent = None
            return

        # Iteratively build internal levels
        level = leaves
        while len(level) > 1:
            parents: list[Node] = []
            j = 0
            m = len(level)
            while j < m:
                group = level[j:j + max_children]
                parent = Node(is_leaf=False)
                parent.children = group
                for child in group:
                    child.parent = parent
                # keys[i] = leftmost_key(children[i+1]) == children[i+1].keys[0] for B+ tree
                sep = array('q', (group[idx].keys[0]
                            for idx in range(1, len(group))))
                parent.keys = sep
                parents.append(parent)
                j += max_children
            level = parents

        # Set root
        self.__root = level[0]
        self.__root.parent = None


if __name__ == '__main__':
    pass
