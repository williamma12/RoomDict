import time
from typing import Optional

from RoomDict.storage_backends import MemoryStorage


class ArbitraryStorage(MemoryStorage):
    def __init__(self, delay: int):
        self.delay = delay

        super().__init__()

    def __setitem__(self, key: str, value: object):
        time.sleep(self.delay)
        
        super().__setitem__(key, value)

    def __getitem__(self, key: str) -> Optional[object]:
        time.sleep(self.delay)
        
        return super().__getitem__(key)

    def __delitem__(self, key: str):
        time.sleep(self.delay)
        
        super().__delitem__(key)

    def __contains__(self, key: str) -> bool:
        time.sleep(self.delay)
        
        return super().__contains__(key)
