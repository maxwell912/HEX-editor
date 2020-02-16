class linked_list:
    head = None

    def __init__(self, value, prev_e=None, next_e=None):
        if linked_list.head is None:
            linked_list.head = self
        self.value = value
        self.next = next_e
        self.prev = prev_e

    @staticmethod
    def range(start, length):
        cur_el = linked_list.head
        if cur_el is None:
            return 0, 0
        while start >= cur_el.value[1] - cur_el.value[0]:
            start -= cur_el.value[1] - cur_el.value[0]
            cur_el = cur_el.next
            if cur_el is None:
                return 0, 0
        while cur_el is not None and length > 0:
            start = cur_el.value[0] + start
            leaf = cur_el.value[1] - start
            c_len = min(leaf, length)
            yield start, start + c_len
            length -= c_len
            start = 0
            cur_el = cur_el.next

    @staticmethod
    def add(data_pos, file_pos):
        data_pos -= 1
        leaf = linked_list([file_pos, file_pos + 1])
        cur_el = linked_list.head
        if cur_el == leaf:
            return
        while data_pos > cur_el.value[1] - cur_el.value[0]:
            data_pos -= cur_el.value[1] - cur_el.value[0]
            cur_el = cur_el.next
            if cur_el is None:
                raise Exception('OutOfBounds')
        if data_pos == 0:
            leaf.prev = cur_el.prev
            leaf.next = cur_el
            if cur_el.prev is not None:
                cur_el.prev.next = leaf
            else:
                linked_list.head = leaf
            cur_el.prev = leaf
            if cur_el.value[0] == cur_el.value[1]:
                linked_list.del_leaf(cur_el)
        elif data_pos == cur_el.value[1] - cur_el.value[0]:
            leaf.prev = cur_el
            leaf.next = cur_el.next
            if cur_el.next is not None:
                cur_el.next.prev = leaf
            cur_el.next = leaf
        else:
            data_pos = data_pos + cur_el.value[0]
            l3 = linked_list([data_pos, cur_el.value[1]])
            l3.next = cur_el.next
            cur_el.value[1] = data_pos
            leaf.prev = cur_el
            leaf.next = l3
            l3.prev = leaf
            cur_el.next = leaf
            leaf.next = l3
        linked_list._check_neib(leaf)

    @staticmethod
    def change(data_pos, file_pos):
        p, n = linked_list.remove(data_pos)
        leaf = linked_list([file_pos, file_pos + 1],
                           p, n)
        if p is not None:
            p.next = leaf
        else:
            linked_list.head = leaf
        if n is not None:
            n.prev = leaf
        linked_list._check_neib(leaf)

    @staticmethod
    def remove(data_pos):
        cur_el = linked_list.head
        while data_pos > cur_el.value[1] - cur_el.value[0]:
            data_pos -= cur_el.value[1] - cur_el.value[0]
            cur_el = cur_el.next
            if cur_el is None:
                raise Exception('OutOfBounds')
        if data_pos == 0:
            cur_el.value[0] += 1
            if cur_el.value[0] == cur_el.value[1]:
                linked_list.del_leaf(cur_el)
            return cur_el.prev, cur_el
        elif data_pos == cur_el.value[1] - cur_el.value[0]:
            cur_el.value[1] -= 1
            if cur_el.value[1] == cur_el.value[0]:
                linked_list.del_leaf(cur_el)
            return cur_el.prev, cur_el.next
        else:
            d = data_pos + cur_el.value[0]
            leaf = linked_list([d, cur_el.value[1]],
                               cur_el, cur_el.next)
            cur_el.value[1] = d - 1
            cur_el.next = leaf
            if cur_el.value[0] == cur_el.value[1]:
                linked_list.del_leaf(cur_el)
                cur_el = cur_el.prev
            return cur_el, leaf

    @staticmethod
    def del_leaf(leaf):
        if leaf.next is not None:
            leaf.next.prev = leaf.prev
        if leaf.prev is not None:
            leaf.prev.next = leaf.next
        if linked_list.head == leaf:
            linked_list.head = leaf.next
        if leaf.next is not None:
            linked_list._check_neib(leaf.next)
        elif leaf.prev is not None:
            linked_list._check_neib(leaf.prev)

    @staticmethod
    def _check_neib(leaf):
        if leaf.prev is not None and leaf.value[0] == leaf.prev.value[1]:
            new_leaf = linked_list([leaf.prev.value[0], leaf.value[1]],
                                   leaf.prev.prev, leaf.next)
            if leaf.prev.prev is not None:
                leaf.prev.prev.next = new_leaf
            if leaf.next is not None:
                leaf.next.prev = new_leaf
            if leaf.prev == linked_list.head:
                linked_list.head = new_leaf
        elif (leaf.next is not None and
              leaf.value[1] == leaf.next.value[0]):
            new_leaf = linked_list([leaf.value[0], leaf.next.value[1]],
                                   leaf.prev, leaf.next.next)
            if leaf.prev is not None:
                leaf.prev.next = new_leaf
            if leaf.next.next is not None:
                leaf.next.next.prev = new_leaf

    def __str__(self):
        s = ''
        cur_el = linked_list.head
        while cur_el is not None:
            s += str(cur_el.value)
            cur_el = cur_el.next
        return s
