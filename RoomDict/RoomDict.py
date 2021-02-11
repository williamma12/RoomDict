from collections.abc import Iterable, MutableMapping
import os
import shelve
from typing import Union

from RoomDict.caches.LRUCache import LRUCache


class RoomDict(MutableMapping):
    def __init__(self, max_cache_size: int = None):
        self.max_cache_size = max_cache_size
        self.size = 0
        self.valid = False

    def __enter__(self):
        self.valid = True

        self.cache = LRUCache(self.max_cache_size)

        # Create shelve kv-store.
        self.directory = ".RoomDict"
        self.out_of_mem_file = "RoomDict"
        os.mkdir(self.directory)
        self.kv_store = shelve.open(f"{self.directory}/{self.out_of_mem_file}")

    def __exit__(self, exc_type, exc_value, traceback):
        self.kv_store.close()

    def check_valid(self):
        if not self.valid:
            raise ValueError("RoomDict has not been opened.")

    def __len__(self):
        return self.size

    def __setitem__(self, key: str, value: object):
        """Put key with associated value to dict.

        Parameters
        ----------
        key : str
            Unique key to the value.
        value : object
            Value to store with key.
        """
        self.check_valid()
        self.size += 1

        evicted = self.cache.put(key, value)

        if evicted is not None:
            self.kv_store[key] = value

    def __getitem__(self, key: str):
        """Get key from dict.

        Parameters
        ----------
        key : str
            Key to get the value.
        """
        result = self.cache.get(key)

        if result is None:
            result = self.kv_store[key]
        else:
            result = result.value

        return result

    def __delitem__(self, key: str):
        """Removes item from dict.

        Parameters
        ----------
        key : str
            Key to remove the item.
        """
        if key in self.cache:
            del self.cache[key]
        else:
            del self.kv_store

    def __iter__(self) -> Iterable[Union[str, object]]:
        raise NotImplementedError

    def __contains__(self, key: str) -> bool:
        return key in self.cache or key in self.kv_store
