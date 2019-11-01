"""
A feladat:
“van egy 1001 elemü tömböd, amiben egytől ezerig vannak különböző számok
hogyan találnád meg a duplikátumot ezek között a számok között segédváltozó nélkül”

Matekos megoldás:
a tömb értékéből kivonjuk a számok összegét egytől ezerig
sum(tomb) - (1 + n) / 2 * n

Algoritmizalt megoldasra egy koncepcio:
- a tömböt egy zárt(utolso elem pointere az elsőre mutat) láncolt listaként reprezentáljuk
- cserelgetessel rendezzük a listát - ami által egymás mellé kerül a két azonos érték
"""
import random
ARRAY_SIZE = 42


class Node:
    """
    Node object for LinkedList
    """
    def __init__(self, value=None, next_node=None):
        self.value = value
        self.next_node = next_node

    def __str__(self):
        return str(self.value)


class LinkedList:
    """
    linked list (close with close_the_ring())
    """
    def __init__(self):
        self.head = None
        self.size = 0
        self.is_closed = False

    def __str__(self):
        if self.size == 0:
            return "[]"
        if self.size == 1:
            return str(self.head.value)
        node = self.head
        string_value = "["
        for nothing in range(self.size - 1):
            string_value += "{0}, ".format(node.value)
            node = node.next_node
        string_value += "{0}]".format(node.value)
        return string_value

    def insert(self, value):
        new_node = Node(value)
        new_node.next_node = self.head
        self.size += 1
        self.head = new_node

    def append(self, value):
        if self.head is None:
            self.insert(value)
        else:
            node = self.last_node()
            new_node = Node(value)
            self.size += 1
            node.next_node = new_node

    def last_node(self):
        if self.head is None:
            return None
        if self.is_closed:
            until = self.head
        else:
            until = None
        node = self.head
        while node.next_node is not until:
            node = node.next_node
        return node

    def close_the_ring(self):
        lastnode = self.last_node()
        lastnode.next_node = self.head
        self.is_closed = True


def main():
    # n + 1 elemszamu tomb elkeszitese, egy duplikatummal
    array = list(range(1, ARRAY_SIZE + 1))
    array.append(random.randint(1, len(array)))
    random.shuffle(array)
    print("Original Array:\n{0}".format(array))

    # a tomb attoltese egy lancolt listaba:
    llist = LinkedList()
    for val in array:
        llist.append(val)
    llist.close_the_ring()
    print("Linked list:\n{0}".format(llist))

    # a duplikatum detektalasa seged valtozo nelkul egy konstans ertekkel
    while llist.head.value != llist.head.next_node.value:
        if (llist.head.value < llist.head.next_node.value) and \
                not (llist.head.value == llist.head.value / llist.head.value
                     and llist.head.next_node.value == ARRAY_SIZE):
            llist.head.value = llist.head.value + llist.head.next_node.value
            llist.head.next_node.value = llist.head.value - llist.head.next_node.value
            llist.head.value = llist.head.value - llist.head.next_node.value
        else:
            llist.head = llist.head.next_node
    print("Semi-sorted:\n{0}".format(llist))
    print("Duplicated item: {0}".format(llist.head))


if __name__ == "__main__":
    main()
