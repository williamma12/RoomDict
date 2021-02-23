import os
import shelve
from typing import Optional

from RoomDict.storage_backends.GenericStorage import GenericStorage


class DiskStorage(GenericStorage):
    def __init__(
        self, directory: str = ".RoomDict", fname: str = "RoomDict.pkl"
    ):  # noqa: E501
        self.directory = directory
        self.path = "{}/{}".format(self.directory, fname)

        super().__init__()

    def open(self):
        if not os.path.exists(self.path):
            os.mkdir(self.directory)

    def close(self, exc_type=None, exc_value=None, traceback=None):
        if os.path.exists(self.path):
            os.remove(self.path)
            os.rmdir(self.directory)

        super()._close()

    def __setitem__(self, key: str, value: object):
        self.size += 1
        with shelve.open(self.path, writeback=False) as kv_store:
            kv_store[key] = value

    def __getitem__(self, key: str) -> Optional[object]:
        with shelve.open(self.path, writeback=False) as kv_store:
            return kv_store[key]

    def __delitem__(self, key: str):
        with shelve.open(self.path, writeback=False) as kv_store:
            if key in kv_store:
                self.size -= 1

            del kv_store[key]

    def __iter__(self):
        raise NotImplementedError

    def __contains__(self, key: str) -> bool:
        with shelve.open(self.path, writeback=False) as kv_store:
            return key in kv_store
