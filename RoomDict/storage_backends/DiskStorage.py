import os
import shelve

from RoomDict.storage_backends.GenericStorage import GenericStorage


class DiskStorage(GenericStorage):
    def __init__(
        self, directory: str = ".RoomDict", fname: str = "RoomDict.pkl"
    ):  # noqa: E501
        self.directory = directory
        self.path = f"{self.directory}/{fname}"

        super().__init__()

    def open(self):
        if not os.path.exists(self.path):
            os.mkdir(self.directory)
        kv_store = shelve.open(self.path, writeback=False)

        super()._open(kv_store)

        # This is a hack to get the typing right.
        self.kv_store: shelve.Shelf

    def close(self, exc_type=None, exc_value=None, traceback=None):
        self.kv_store.close()

        if os.path.exists(self.path):
            os.remove(self.path)
            os.rmdir(self.directory)

        super()._close()
