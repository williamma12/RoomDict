import os
import shelve

from RoomDict.LRUCache import CacheRecord, LRUCache


# TODO: Update RoomDict to be a mutablemapping.
class RoomDict:
    def __init__(self, max_cache_size: int = None):
        self.max_cache_size = max_cache_size
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

    def put(self, key: str, value: object):
        """Put key with associated value to dict.

        Parameters
        ----------
        key : str
            Unique key to the value.
        value : object
            Value to store with key.
        """
        self.check_valid()

        evicted = self.cache.put(CacheRecord(key, value))

        if evicted is not None:
            self.kv_store[key] = value

    def get(self, key: str):
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
