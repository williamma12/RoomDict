import abc
from dataclasses import dataclass
from collections.abc import Iterable, MutableMapping
from typing import Optional, Union
import uuid

from RoomDict.storage_backends.GenericStorage import GenericStorage
from RoomDict.membership_tests.GenericMembership import GenericMembership


@dataclass
class Record:
    key: str
    value: object


class GenericCache(MutableMapping):
    def __init__(
        self, storage_manager: GenericStorage, membership_test: GenericMembership
    ):
        self.size = 0
        self.storage_manager = storage_manager
        self.membership_test = membership_test

    @abc.abstractmethod
    def put(self, key: str, value: object) -> Optional[Union[str, object]]:
        """Puts a key and value to the cache.

        Parameters
        ----------
        key : str
            strey to add to the cache.
        value : object
            objectalue to add with the key to the cache.

        Returns
        -------
        Returns the evicted Record. If nothing was evicted, then None.
        """
        pass

    @abc.abstractmethod
    def get(self, key: str) -> Optional[object]:
        """Gets the associated record from cache if exists.

        Parameters
        ----------
        key : str
            strey to get from cache.

        Returns
        -------
        Record associated with the key if it exists, else None.
        """
        pass

    @abc.abstractmethod
    def __delitem__(self, key: str):
        pass

    @abc.abstractmethod
    def __iter__(self) -> Iterable:
        pass

    def __contains__(self, key: str) -> bool:
        if key not in self.membership_test:
            return key in self.storage_manager
        else:
            return True

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, key: str) -> object:
        result = self.get(key)
        if result is None:
            raise ValueError(f"{key} does not exist.")
        return result

    def __setitem__(self, key: str, value: object):
        self.membership_test.add(key)
        self.put(key, value)
