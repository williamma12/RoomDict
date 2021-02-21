import abc
from collections.abc import MutableMapping
from typing import Optional


class GenericStorage(MutableMapping):
    def __init__(self):
        self.valid = False
        self.size = 0

    def _check_valid(self):
        if not self.valid:
            raise ValueError("RoomDict has not been opened.")

    def __len__(self):
        return self.size

    @abc.abstractmethod
    def open(self):
        pass

    @abc.abstractmethod
    def close(self, exc_type = None, exc_value = None, traceback = None):
        pass

    def _open(self, kv_store: MutableMapping):
        self.kv_store = kv_store
        self.valid = True

    def _close(self):
        self.valid = False

    def __setitem__(self, key: str, value: object):
        self._check_valid()

        self.size += 1
        self.kv_store[key] = value

    def __getitem__(self, key: str) -> Optional[object]:
        self._check_valid()

        return self.kv_store[key]

    def __delitem__(self, key: str):
        self._check_valid()

        if key in self.kv_store:
            self.size -= 1

        del self.kv_store[key]

    def __iter__(self):
        self._check_valid()

        iter(self.kv_store)

    def __contains__(self, key: str) -> bool:
        self._check_valid()

        return key in self.kv_store
