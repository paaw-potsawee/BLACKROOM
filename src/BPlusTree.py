class Node:
    def __init__(self, order: int, is_leaf: bool = True):
        self.__order: int = order
        self.__values = []
        self.__keys = []
        self.__next_key = None
        self.__parent = None
        self.__is_leaf = is_leaf

    def insert(self, val):
        if len(self.__values) > 0:
            temp = self.__values
            for i in range(len(temp)):
                if val < self.__values[i]:
                    self.__values.insert(i, val)
                    break
                elif i + 1 == len(temp):
                    self.__values.append(val)
                    break
        else:
            self.__values.append(val)

    def __str__(self):
        return f"{" ".join(list(map(str, (self.values))))}"

    @property
    def keys(self): return self.__keys
    @keys.setter
    def keys(self, data: list): self.__keys = data

    @property
    def values(self): return self.__values
    @values.setter
    def values(self, data: list): self.__values = data

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

    def append_val(self, data): self.__values.append(data)

    def append_key(self, data): self.__keys.append(data)


class BPlusTree:
    def __init__(self, order: int = 4):
        if order < 3:
            raise ValueError('B+ tree order should not  less than 3')
        self.__root = Node(order, is_leaf=True)

    def insert(self, val):
        self._insert(self.__root, val)

    def _insert(self, node: Node, val):
        # search for leaf node
        leaf_node = self.search_leaf(node, val)
        leaf_node.insert(val)
        order = leaf_node.order

        if len(leaf_node.values) > order - 1:
            mid = len(leaf_node.values) // 2
            new_leaf = Node(order, is_leaf=True)
            new_leaf.values = leaf_node.values[mid:]
            leaf_node.values = leaf_node.values[:mid]
            new_leaf.next_key = leaf_node.next_key
            leaf_node.next_key = new_leaf

            # case where leaf node is root
            if leaf_node.parent is None:
                new_root = Node(order, is_leaf=False)
                new_root.values = [new_leaf.values[0]]
                new_root.keys = [leaf_node, new_leaf]
                leaf_node.parent = new_root
                new_leaf.parent = new_root
                self.__root = new_root
            # case where leaf node has parent (continue to check recursively)
            else:
                self._insert_separator(
                    leaf_node.parent, new_leaf.values[0], new_leaf)

    def _insert_separator(self, parent: Node, val, new_child: Node):
        # insert value and new child to parent
        i = 0
        while i < len(parent.values) and val > parent.values[i]:
            i += 1
        parent.values.insert(i, val)
        parent.keys.insert(i + 1, new_child)
        new_child.parent = parent

        # check if parent overflows (if split recursively)
        if len(parent.values) > parent.order - 1:
            mid = len(parent.values) // 2
            promoted_val = parent.values[mid]

            # create new internal node
            new_node = Node(parent.order, is_leaf=False)
            new_node.values = parent.values[mid + 1:]
            new_node.keys = parent.keys[mid + 1:]
            # point child to new parent
            for child in new_node.keys:
                child.parent = new_node

            parent.values = parent.values[:mid]
            parent.keys = parent.keys[:mid + 1]

            if parent.parent is None:
                # root
                new_root = Node(parent.order, is_leaf=False)
                new_root.values = [promoted_val]
                new_root.keys = [parent, new_node]
                parent.parent = new_root
                new_node.parent = new_root
                self.__root = new_root
            else:
                self._insert_separator(parent.parent, promoted_val, new_node)

    def search_leaf(self, node: Node, val):
        while not node.is_leaf:
            if val >= node.values[-1]:
                node = node.keys[-1]
            else:
                for i in range(len(node.values)):
                    if val < node.values[i]:
                        node = node.keys[i]
                        break
        return node

    def print_tree(self):
        print('print entire tree')
        self._print_tree(self.__root, 0)

    def _print_tree(self, node: Node, level: int):
        if node is not None:
            print(f'{level} -> {node}')
            for key in node.keys:
                self._print_tree(key, level + 1)

    def print_leaf(self):
        print('print all data in tree')
        node = self.__root
        while not node.is_leaf:
            node = node.keys[0]
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
