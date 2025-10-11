from typing import Optional, Any
from array import array


class Node:
    def __init__(self, is_leaf: bool = True):
        self.__keys: array = array('i')
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
    def keys(self, data: list): self.__keys = array('i', data)

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
    def __init__(self, order: int = 4):
        if order < 3:
            raise ValueError('B+ tree order should not  less than 3')
        self.__order: int = order
        self.__min_key: int = -(-self.__order // 2) - 1
        self.__root: Node = Node(is_leaf=True)

    @property
    def root(self): return self.__root

    def insert(self, data):
        self._insert(self.__root, data[0], data[1])

    def _insert(self, node: Node, key, val=None):
        # search for leaf node
        leaf_node = self.search_leaf(node, key)
        if key in leaf_node.keys:
            raise ValueError(
                f'Insertion into existing room ### this is for debug calculate guest room only {key}')
        leaf_node.insert(key, val)

        if len(leaf_node.keys) > self.__order - 1:
            mid = len(leaf_node.keys) // 2
            new_leaf = Node(is_leaf=True)
            new_leaf.keys = list(leaf_node.keys[mid:])
            leaf_node.keys = list(leaf_node.keys[:mid])
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
            new_node.keys = list(parent.keys[mid + 1:])
            new_node.children = parent.children[mid + 1:]
            # point child to new parent
            for child in new_node.children:
                child.parent = new_node

            parent.keys = list(parent.keys[:mid])
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
        leaf_node = self.search_leaf(self.__root, val)
        try:
            idx = leaf_node.keys.index(val)
        except ValueError:
            print('not found')
            return -1

        leaf_node.keys.remove(val)
        if leaf_node.is_leaf:
            leaf_node.children.pop(idx)

        parent = leaf_node.parent
        # if leaf node is root
        if parent is None:
            return

        # if leaf node has at least min_key
        if leaf_node.get_key_len() >= self.__min_key:
            # if first value of keys update separator recursively
            self.__update_separator(leaf_node)
            return

        # underflow
        # try borrow from sibling
        left, right, leaf_idx = parent.get_siblings(leaf_node)
        # try from left first
        if left and left.get_key_len() > self.__min_key:
            leaf_node.keys.insert(0, left.keys.pop())
            if left.is_leaf and len(left.children) > 0:
                leaf_node.children.insert(0, left.children.pop())
            self.__update_separator(leaf_node)
            return
        # try from right if left failed
        if right and right.get_key_len() > self.__min_key:
            leaf_node.keys.append(right.keys.pop(0))
            if right.is_leaf and len(right.children) > 0:
                leaf_node.children.append(right.children.pop(0))
            self.__update_separator(right)
            self.__update_separator(leaf_node)
            return

        # merge with sibing try merge with left (if exists) then with right
        if left:
            # merge with left node
            self.__merge_node(left, leaf_node, parent, leaf_idx - 1)
            if len(parent.keys) < self.__min_key:
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
            # merge two internals
            left.keys.append(parent.keys[separator_idx])
            left.keys.extend(right.keys)
            left.children.extend(right.children)
            for child in right.children:
                child.parent = left

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
        if left and len(left.keys) > self.__min_key:
            borrow_key = parent.keys[idx - 1]
            # insert the separator at front of node.keys
            node.keys.insert(0, borrow_key)
            # move last child from left into node
            child = left.children.pop()
            node.children.insert(0, child)
            child.parent = node
            # replace parent separator with left's last key
            parent.keys[idx - 1] = left.keys.pop()
            return

        # borrow from right
        if right and len(right.keys) > self.__min_key:
            borrow_key = parent.keys[idx]
            node.keys.append(borrow_key)
            child = right.children.pop(0)
            node.children.append(child)
            child.parent = node
            parent.keys[idx] = right.keys.pop(0)
            return

        # merge with left
        if left:
            self.__merge_node(left, node, parent, idx - 1)
            if len(parent.keys) < self.__min_key:
                self.__handle_internal_underflow(parent)
            return

        # merge with right
        if right:
            self.__merge_node(node, right, parent, idx)
            if len(parent.keys) < self.__min_key:
                self.__handle_internal_underflow(parent)
            return

    def __update_separator(self, node: Node):
        parent = node.parent
        if parent is None:
            return

        for i in range(len(parent.keys)):
            parent.keys[i] = self.__leftmost_key(parent.children[i + 1])
        # recurse upward
        self.__update_separator(parent)

    def __leftmost_key(self, node: Node):
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0]

    def process_room_number(self, cal_func):
        if self.__root is None or len(self.__root.keys) == 0:
            return
        stack = [self.__root]
        while stack:
            node = stack.pop()
            for i in range(len(node.keys)):
                node.keys[i] = cal_func(node.keys[i])
            if node.is_leaf:
                for i in range(len(node.keys)):
                    node.children[i].current_room_number = node.keys[i]
            else:
                stack.extend(node.children)

    def shift_room_number(self, cal_func, key):
        node = self.__root
        stack = []

        while not node.is_leaf:
            child_idx = self.__binary_search(node.keys, key)
            stack.append((node, child_idx))
            node = node.children[child_idx]

        # perform shift in leaf node
        left = 0
        right = len(node.keys) - 1
        while left < right:
            mid = left + (right - left) // 2
            if key > node.keys[mid]:
                left = mid + 1
            else:
                right = mid

        if len(node.keys) == 0:
            return
        # if room is empty will not shift (ideal should always be shifted)
        if left >= len(node.keys) or key != node.keys[left]:
            return

        start = left if left < len(node.keys) else len(node.keys)
        for i in range(start, len(node.keys)):
            node.keys[i] = cal_func(node.keys[i])
            node.children[i].current_room_number = node.keys[i]

        self.__update_separator(node)
        # shift room after number by 1
        while stack:
            parent, child_idx = stack.pop()
            # update every child of that node
            for i in range(child_idx, len(parent.keys)):
                parent.keys[i] = cal_func(parent.keys[i])

    def search_leaf(self, node: Node, val):
        while not node.is_leaf:
            child_idx = self.__binary_search(node.keys, val)
            node = node.children[child_idx]
        return node

    def __binary_search(self, keys: array, val: int) -> int:
        left, right = 0, len(keys)
        while left < right:
            mid = left + (right - left) // 2
            if keys[mid] <= val:
                left = mid + 1
            else:
                right = mid

        return left

    def get_leftmost_node(self):
        node = self.__root
        while not node.is_leaf:
            node = node.children[0]

        return node

    def search(self, val: int):
        leaf = self.search_leaf(self.__root, val)
        if val in leaf.keys:
            return leaf.children[leaf.keys.index(val)]

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
        node = self.__root
        while not node.is_leaf:
            node = node.children[0]
        self._print_leaf(node)

    def _print_leaf(self, node: Optional[Node]):
        while node is not None:
            for i in range(len(node.keys)):
                print(f'{node.keys[i]: >9d}: {node.children[i]}', end='\n')
            node = node.next_key
        print('')


if __name__ == '__main__':
    class Guest:
        def __init__(self, current_room_number: int, channel: int, arrived_order: int):
            self.__current_room_number = current_room_number
            self.__channel = channel
            self.__arrived_order = arrived_order

        @property
        def current_room_number(self): return self.__current_room_number
        @current_room_number.setter
        def current_room_number(self, n): self.__current_room_number = n

        @property
        def channel(self): return self.__channel

        @property
        def arrived_order(self): return self.__arrived_order

        def __repr__(self) -> str:
            return f"Guest(Room: {self.__current_room_number}, Channel: {self.channel}, Arrived: {self.__arrived_order})"
    tree = BPlusTree()
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    guests = []
    for i in num:
        guests.append((i, Guest(i, 1, 0)))

    for guest in guests:
        tree.insert(guest)

    print('----- tree after insert with guest data ----')
    tree.print_tree()
    tree.print_leaf()

    print('----- tree after delete and insert with guest data ----')
    tree.delete(9)
    tree.shift_room_number(lambda x: x + 1, 9)
    tree.insert((9, Guest(9, 1, 1)))
    tree.print_tree()
    tree.print_leaf()

    # tree.shift_room_number(lambda x: x + 1, 13)
    # tree.insert((13, Guest(13, 1, 1)))
    # tree.shift_room_number(lambda x: x + 1, 12)
    # tree.insert((12, Guest(12, 1, 1)))
    # print('----- tree after shift and insert ----')
    # tree.print_tree()
    # tree.print_leaf()

    # Test deletion
    # tree.delete(2)
    # print('----- tree after delete 2 ----')
    # tree.print_tree()
    # tree.print_leaf()
