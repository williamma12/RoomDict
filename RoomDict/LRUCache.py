from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

HEAD_KEY = "__HEAD__"
TAIL_KEY = "__TAIL__"

@dataclass
class CacheRecord:
    key: str
    value: object

class CacheNode(object):
    def __init__(self, record : CacheRecord, next_node : Optional[CacheNode] = None, prev_node : Optional[CacheNode] = None):
        self.record = record
        self.next = next_node
        self.prev = prev_node

class LRUCache(object):
    def __init__(self, max_size):
        assert max_size > 0, f"Max size should be greater than 0. Max size is {max_size}"

        self.max_size = max_size
        self.curr_size = 0

        self.cache_head = CacheNode(CacheRecord(HEAD_KEY, ""))
        self.cache_tail = CacheNode(CacheRecord(TAIL_KEY, ""))
        self.cache_head.next = self.cache_tail
        self.cache_tail.prev = self.cache_head

        self.directory = {}

    def put(self, record : CacheRecord) -> Optional[CacheRecord]:
        """Puts a key and value to the cache.

        Parameters
        ----------
        record : CacheRecord
            Record to add to the cache.

        Returns
        -------
        Returns the evicted CacheRecord. If nothing was evicted, then None.
        """
        key = record.key

        if key == HEAD_KEY or key == TAIL_KEY:
            raise ValueError("Invalid key names")

        if key in self.directory:
            self.directory[key].record = record
            return None
        
        if self.curr_size < self.max_size:
            self.curr_size += 1
            evicted = None
        else:
            # Evict the last node in the linked list.
            to_evict = self.cache_tail.prev
            last_node = to_evict.prev
            self.cache_tail.prev = last_node
            last_node.next = self.cache_tail

            evicted = to_evict.record

            del self.directory[evicted.key]

        # Set new node as the head of the linked list.
        new_node = CacheNode(record)
        curr_head = self.cache_head.next
        new_node.prev = self.cache_head
        new_node.next = curr_head
        curr_head.prev = new_node
        self.cache_head.next = new_node
        
        self.directory[key] = new_node

        return evicted

    def get(self, key : str) -> Optional[CacheRecord]:
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

        get_node = self.directory[key]
        curr_head = self.cache_head.next

        get_node.prev.next = get_node.next
        get_node.next.prev = get_node.prev
        get_node.next = curr_head
        get_node.prev = self.cache_head
        curr_head.prev = get_node
        self.cache_head.next = get_node

        return get_node.record
