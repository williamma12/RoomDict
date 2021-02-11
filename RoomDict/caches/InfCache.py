from collections.abc import Iterable
from typing import Union

from RoomDict.caches.GenericCache import GenericCache, Record


class InfCache(GenericCache):
    def __init__(self):
        self.directory: dict[str, object] = {}

        super().__init__()

    def put(self, key: str, value: object):
        self.directory[key] = value

    def get(self, key: str) -> Record:
        value = self.directory[key]

        return Record(key, value)

    def __delitem__(self, key: str):
        del self.directory[key]

    def __iter__(self) -> Iterable[Union[str, object]]:
        return iter(self.directory)

    def __contains__(self, key: str) -> bool:
        return key in self.directory
