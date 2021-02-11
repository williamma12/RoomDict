from collections.abc import Iterable
from typing import Optional, Union

from RoomDict.caches.LinkedList import LinkedList, Node
from RoomDict.caches.GenericCache import GenericCache, Record


class LRUCache(GenericCache):
    def __init__(self, max_size):
        assert (
            max_size > 0
        ), f"Max size should be greater than 0. Max size is {max_size}"

        self.max_size = max_size
        self.lru_list = LinkedList()
        self.directory: dict[str, Node] = {}

        super().__init__()

    def put(self, key: str, value: object) -> Optional[Record]:
        record = Record(key, value)

        if key in self.directory:
            self.directory[key].value = record
            return None

        if self.size < self.max_size:
            self.size += 1
            evicted_value = None
        else:
            evicted_value = self.lru_list.pop().value
            if evicted_value is None:
                raise ValueError("No value to evict.")

            del self.directory[evicted_value.key]

        new_list_value = self.lru_list.prepend_value(record)
        self.directory[key] = new_list_value 

        return evicted_value

    def get(self, key: str) -> Optional[Record]:
        if key not in self.directory:
            return None

        node = self.directory[key]
        
        self.lru_list.delete(node)
        self.lru_list.prepend_node(node)

        return node.value

    def __delitem__(self, key: str):
        assert key in self

        self.size -= 1

        node = self.directory[key]
        self.lru_list.delete(node)

        del self.directory[key]

    def __iter__(self) -> Iterable[Union[str, object]]:
        self.record_iter = iter(self.lru_list)
        return self

    def __next__(self) -> Union[str, object]:
        next_record: Record = next(self.record_iter)
        return (next_record.key, next_record.value)

    def __contains__(self, key: str) -> bool:
        return key in self.directory
