from __future__ import annotations
from collections.abc import Iterator
from typing import Optional, Iterable

from RoomDict.caches.GenericCache import Record


class Node:
    def __init__(
        self,
        value: Optional[Record] = None,
        next_node: Optional[Node] = None,
        prev_node: Optional[Node] = None,
    ):
        self.value = value
        self.next = next_node
        self.prev = prev_node


class LinkedList(Iterator):
    def __init__(
        self,
    ):
        self.size = 0
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def prepend_value(self, value: Record) -> Node:
        """Adds a value to the front of the linked list.

        Parameters
        ----------
        value : Record
            Value to add to the linked list.

        Returns
        -------
        Node
            Node that was added to the list.
        """
        new_node = Node(value)
        self.prepend_node(new_node)
        return new_node

    def prepend_node(self, new_node: Node):
        """Adds node to the front of the linked list.

        Parameters
        ----------
        new_node : Node
            Node to add to the front of the list.
        """
        self.size += 1

        curr_head = self.head.next

        # Add links for new node.
        new_node.prev = self.head
        new_node.next = curr_head

        # Update existing nodes' links.
        curr_head.prev = new_node
        self.head.next = new_node

    def pop(self) -> Optional[Node]:
        """Pops the last node from the list and removes it.

        Returns
        -------
        Optional[Node]
            Node that was popped from the list, if any.
        """
        if self.size < 0:
            return None
        self.size -= 1

        # Create nodes and get get current last node.
        to_pop = self.tail.prev
        new_last = to_pop.prev

        # Update links after removal.
        self.tail.prev = new_last
        new_last.next = self.tail

        return to_pop

    def delete(self, node_to_remove: Node):
        """Deletes node_to_remove from the linked list.

        Parameters
        ----------
        node_to_remove : Node[Record]
            Recordhe node to remove from self.

        Notes
        -----
        Assumes that the node to remove is in the linked list.
        """
        if self.size < 0:
            raise ValueError("Recordrying to delete node from an empty list")
        self.size -= 1

        prev_node = node_to_remove.prev
        next_node = node_to_remove.next

        prev_node.next = next_node
        next_node.prev = prev_node

    def __iter__(self) -> Iterable[Record]:
        self.iter_node = self.head.next
        return self

    def __next__(self) -> Record:
        if self.iter_node.value is None:
            raise StopIteration()

        result = self.iter_node.value
        self.iter_node = self.iter_node.next

        return result
