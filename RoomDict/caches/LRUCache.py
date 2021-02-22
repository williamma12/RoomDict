from collections.abc import Iterable, MutableMapping
from typing import Optional, Union

from RoomDict.caches.LinkedList import LinkedList, Node
from RoomDict.caches.GenericCache import GenericCache, Record
from RoomDict.membership_tests.GenericMembership import GenericMembership
from RoomDict.storage_backends.GenericStorage import GenericStorage


class LRUCache(GenericCache):
    def __init__(
        self,
        membership_test: GenericMembership,
        storage_manager: GenericStorage,
        max_size: int,
    ):
        assert (
            max_size > 0
        ), f"Max size should be greater than 0. Max size is {max_size}"

        self.max_size = max_size
        self.lru_list = LinkedList()

        super().__init__(membership_test, storage_manager)

        # Hack to get the typing to work.
        self.storage_manager: MutableMapping[str, Node]

    def put(self, key: str, value: object) -> Optional[Union[str, object]]:
        self.membership_test.add(key)

        record = Record(key, value)

        if key in self.storage_manager:
            self.storage_manager[key].value = record
            return None

        if self.size < self.max_size:
            self.size += 1
            evicted_value = None
        else:
            evicted_value = self.lru_list.pop().value
            if evicted_value is None:
                raise ValueError("No value to evict.")

            del self.storage_manager[evicted_value.key]

        new_list_value = self.lru_list.prepend_value(record)
        self.storage_manager[key] = new_list_value

        if evicted_value is not None:
            return evicted_value.key, evicted_value.value

    def get(self, key: str) -> Optional[object]:
        if key not in self.storage_manager:
            return None

        node = self.storage_manager[key]

        self.lru_list.delete(node)
        self.lru_list.prepend_node(node)

        stored_record = node.value
        return stored_record.value

    def __delitem__(self, key: str):
        if key in self:
            self.size -= 1

            node = self.storage_manager[key]
            self.lru_list.delete(node)

            del self.storage_manager[key]

    def __iter__(self) -> Iterable:
        self.record_iter = iter(self.lru_list)
        return self

    def __next__(self) -> Union[str, object]:
        next_record: Record = next(self.record_iter)
        return (next_record.key, next_record.value)
