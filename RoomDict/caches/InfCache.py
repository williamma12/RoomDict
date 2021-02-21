from collections.abc import Iterable
from typing import Union

from RoomDict.caches.GenericCache import GenericCache
from RoomDict.storage_backends.GenericStorage import GenericStorage


class InfCache(GenericCache):
    def put(self, key: str, value: object):
        self.storage_manager[key] = value

    def get(self, key: str) -> object:
        value = self.storage_manager[key]

        return value

    def __delitem__(self, key: str):
        del self.storage_manager[key]

    def __iter__(self) -> Union[str, object]:
        return iter(self.storage_manager)
