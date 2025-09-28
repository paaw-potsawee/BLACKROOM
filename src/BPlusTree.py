class Node:
    def __init__(self, order: int, is_leaf: bool = True):
        self.__order: int = order
        self.__keys = []         # was __values
        self.__children = []     # was __keys
        self.__next_key = None
        self.__parent = None
        self.__is_leaf = is_leaf

    def insert(self, val):
        if len(self.__keys) > 0:
            temp = self.__keys
            for i in range(len(temp)):
                if val < self.__keys[i]:
                    self.__keys.insert(i, val)
                    break
                elif i + 1 == len(temp):
                    self.__keys.append(val)
                    break
        else:
            self.__keys.append(val)

    def __str__(self):
        return f"{" ".join(list(map(str, (self.keys))))}"

    @property
    def children(self): return self.__children
    @children.setter
    def children(self, data: list): self.__children = data

    @property
    def keys(self): return self.__keys
    @keys.setter
    def keys(self, data: list): self.__keys = data

    @property
    def parent(self): return self.__parent
    @parent.setter
    def parent(self, data): self.__parent = data

    @property
    def is_leaf(self): return self.__is_leaf

    @property
    def order(self): return self.__order

    @property
    def next_key(self): return self.__next_key
    @next_key.setter
    def next_key(self, data): self.__next_key = data

    def append_key(self, data): self.__keys.append(data)

    def append_child(self, data): self.__children.append(data)


class BPlusTree:
    def __init__(self, order: int = 4):
        if order < 3:
            raise ValueError('B+ tree order should not  less than 3')
        self.__root = Node(order, is_leaf=True)

    @property
    def root(self): return self.__root

    def insert(self, val):
        self._insert(self.__root, val)

    def _insert(self, node: Node, val):
        # search for leaf node
        leaf_node = self.search_leaf(node, val)
        leaf_node.insert(val)
        order = leaf_node.order

        if len(leaf_node.keys) > order - 1:
            mid = len(leaf_node.keys) // 2
            new_leaf = Node(order, is_leaf=True)
            new_leaf.keys = leaf_node.keys[mid:]
            leaf_node.keys = leaf_node.keys[:mid]
            new_leaf.next_key = leaf_node.next_key
            leaf_node.next_key = new_leaf

            # case where leaf node is root
            if leaf_node.parent is None:
                new_root = Node(order, is_leaf=False)
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
        if len(parent.keys) > parent.order - 1:
            mid = len(parent.keys) // 2
            promoted_val = parent.keys[mid]

            # create new internal node
            new_node = Node(parent.order, is_leaf=False)
            new_node.keys = parent.keys[mid + 1:]
            new_node.children = parent.children[mid + 1:]
            # point child to new parent
            for child in new_node.children:
                child.parent = new_node

            parent.keys = parent.keys[:mid]
            parent.children = parent.children[:mid + 1]

            if parent.parent is None:
                # root
                new_root = Node(parent.order, is_leaf=False)
                new_root.keys = [promoted_val]
                new_root.children = [parent, new_node]
                parent.parent = new_root
                new_node.parent = new_root
                self.__root = new_root
            else:
                self._insert_separator(parent.parent, promoted_val, new_node)

    def delete(self, val):
        leaf_node = self.search_leaf(self.__root, val)
        # remove value from leaf node
        n = len(leaf_node.keys)
        for i in range(n):
            if val == leaf_node.keys[i]:
                leaf_node.keys.remove(i)
                break
            if i == n - 1:
                print('not found')
                return -1
        # case where leaf still has other node
        if len(leaf_node.keys) != 0:
            pass
        # update parent after deleting
        # ???? how to

    def search_leaf(self, node: Node, val):
        while not node.is_leaf:
            if val >= node.keys[-1]:
                node = node.children[-1]
            else:
                for i in range(len(node.keys)):
                    if val < node.keys[i]:
                        node = node.children[i]
                        break
        return node

    def print_tree(self):
        print('print entire tree')
        self._print_tree(self.__root, 0)

    def _print_tree(self, node: Node, level: int):
        if node is not None:
            print(f'{level} -> {node}')
            for child in node.children:
                self._print_tree(child, level + 1)

    def print_leaf(self):
        print('print all data in tree')
        node = self.__root
        while not node.is_leaf:
            node = node.children[0]
        self._print_leaf(node)

    def _print_leaf(self, node: Node):
        while node.next_key:
            print(f'{node}', end=' -> ')
            node = node.next_key
        print(f'{node}')


if __name__ == '__main__':
    tree = BPlusTree()
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)
    tree.insert(8)
    tree.insert(9)
    tree.insert(10)
    tree.insert(11)
    tree.insert(12)
    tree.insert(13)
    tree.insert(14)
    tree.insert(15)
    tree.insert(16)
    tree.print_tree()
    tree.print_leaf()
