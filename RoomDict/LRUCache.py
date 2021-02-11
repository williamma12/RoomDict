from __future__ import annotations
from typing import Mapping, Optional

from RoomDict.LinkedList import CacheRecord, CacheLinkedList, Node


# TODO: Update LRUCache to be a mutablemapping.
# TODO: LRUCache should be a child of an ABC container class.
class LRUCache(object):
    def __init__(self, max_size):
        assert (
            max_size > 0
        ), f"Max size should be greater than 0. Max size is {max_size}"

        self.max_size = max_size
        self.curr_size = 0
        self.lru_list = CacheLinkedList()
        self.directory: dict[str, Node] = {}

    def put(self, key: str, value: object) -> Optional[CacheRecord]:
        """Puts a key and value to the cache.

        Parameters
        ----------
        record : CacheRecord
            Record to add to the cache.

        Returns
        -------
        Returns the evicted CacheRecord. If nothing was evicted, then None.
        """
        record = CacheRecord(key, value)

        if key in self.directory:
            self.directory[key].value = record
            return None

        if self.curr_size < self.max_size:
            self.curr_size += 1
            evicted_value = None
        else:
            evicted_value = self.lru_list.pop().value
            if evicted_value is None:
                raise ValueError("No value to evict.")

            del self.directory[evicted_value.key]

        new_list_value = self.lru_list.prepend_value(record)
        self.directory[key] = new_list_value 

        return evicted_value

    def get(self, key: str) -> Optional[CacheRecord]:
        """Gets the associated record from cache if exists.

        Parameters
        ----------
        key : str
            Key to get from cache.

        Returns
        -------
        CacheRecord associated with the key if it exists, else None.
        """
        if key not in self.directory:
            return None

        node = self.directory[key]
        
        self.lru_list.delete(node)
        self.lru_list.prepend_node(node)

        return node.value

    def __delitem__(self, key: str):
        """Deletes item from LRU Cache.

        Parameters
        ----------
        key : str
            Key to delete from the cache.

        Notes
        -----
        Assumes that the key is in the cache.
        """
        node = self.directory[key]
        self.lru_list.delete(node)

        del self.directory[key]
    
    def __contains__(self, key: str) -> bool:
        """Check if key is in this cache layer.

        Parameters
        ----------
        key : str
            Key to look for.

        Returns
        -------
        bool
            True if in the cache. False otherwise.
        """
        return key in self.directory
