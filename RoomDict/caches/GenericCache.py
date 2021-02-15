import abc
from dataclasses import dataclass
from collections.abc import Iterable, MutableMapping
from typing import Optional, Union


@dataclass
class Record:
    key: str
    value: object


class GenericCache(MutableMapping):
    def __init__(self):
        self.size = 0

    @abc.abstractmethod
    def put(self, key: str, value: object) -> Optional[Record]:
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
    def get(self, key: str) -> Optional[Record]:
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

    @abc.abstractmethod
    def __contains__(self, key: str) -> bool:
        pass

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, key: str) -> object:
        result = self.get(key)
        if result is None:
            raise ValueError(f"{key} does not exist.")
        return result.value

    def __setitem__(self, key: str, value: object):
        self.put(key, value)
