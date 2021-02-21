from typing import Optional

from RoomDict.storage_backends.GenericStorage import GenericStorage


class MemoryStorage(GenericStorage):
    def open(self):
        kv_store = {}

        super()._open(kv_store)

    def close(self, exc_type = None, exc_value = None, traceback = None):
        self.kv_store.clear()

        super()._close()
