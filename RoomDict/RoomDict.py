from collections.abc import Iterable, MutableMapping
import os
import shelve
from typing import List, Optional, Union

from RoomDict.caches import LRUCache, InfCache
from RoomDict.storage_backends import DiskStorage, MemoryStorage

STORAGE_BACKEND_MAPPING = {
    "memory": MemoryStorage,
    "disk": DiskStorage,
}
CACHE_POLICY_MAPPING = {
    "lru": LRUCache,
    "none": InfCache,
}


# TODO: Add membership test for initialization here and caches.
class RoomDict(MutableMapping):
    def __init__(
        self,
        cache_policies: List[str],
        storage_backends: List[str],
        cache_policies_kwargs: Optional[List[dict]] = None,
        storage_backends_kwargs: Optional[List[dict]] = None,
    ):
        """Initialize a RoomDict with the given storage_backends and cache_policies.

        Parameters
        ----------
        storage_backends : List[str]
            List of storage backend strings. Order implies the storage hierarchy.
        cache_policies : List[str]
            List of cache policy strings. Corresponds to the storage_backends
        storage_backends_kwargs : List[dict]
            Dictionary of storage backend initialization kwargs.
        cache_policies_kwargs: List[dict]
            Dictionary of cache policies initialization kwargs.

        Returns
        -------
        RoomDict
            RoomDict with chosen parameters.
        """
        assert len(storage_backends) == len(
            cache_policies
        ), "Must have equal numbers of storage backends and cache policies."

        if storage_backends_kwargs is None:
            storage_backends_kwargs = []
        if cache_policies_kwargs is None:
            cache_policies_kwargs = []

        if len(storage_backends_kwargs) != len(storage_backends):
            storage_backends_kwargs += [{}] * (
                len(storage_backends) - len(storage_backends_kwargs)
            )
        if len(cache_policies_kwargs) != len(cache_policies):
            cache_policies_kwargs += [{}] * (
                len(cache_policies) - len(cache_policies_kwargs)
            )

        self._initialize_cache_and_storage(
            cache_policies,
            storage_backends,
            cache_policies_kwargs,
            storage_backends_kwargs,
        )

    def _initialize_cache_and_storage(
        self,
        cache_policies: List[str],
        storage_backends: List[str],
        cache_policies_kwargs: List[dict],
        storage_backends_kwargs: List[dict],
    ):
        self.caches = []
        self.storage_backends = []
        for storage_backend, cache_policy, storage_kwargs, cache_kwargs, in zip(
            storage_backends,
            cache_policies,
            storage_backends_kwargs,
            cache_policies_kwargs,
        ):
            storage_backend = STORAGE_BACKEND_MAPPING[storage_backend]
            cache_policy = CACHE_POLICY_MAPPING[cache_policy]

            storage_backend = storage_backend(**storage_kwargs)
            self.caches.append(cache_policy(storage_backend, **cache_kwargs))
            self.storage_backends.append(storage_backend)

    def __enter__(self):
        for storage_backend in self.storage_backends:
            storage_backend.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for storage_backend in self.storage_backends:
            storage_backend.close(exc_type, exc_value, traceback)

    def __len__(self):
        size = 0
        for cache in self.caches:
            size += len(cache)

    def __setitem__(self, key: str, value: int):
        if key in self:
            old_value = self.pop(key)
            value += value

        evicted = (key, value)
        for cache in self.caches:
            evicted = cache.put(*evicted)
            if evicted is None:
                return None

        return evicted

    def __getitem__(self, key: str):
        for cache in self.caches:
            if key in cache:
                return cache.get(key)

    def __delitem__(self, key: str):
        for cache in self.caches:
            if key in cache:
                del cache[key]

    def __iter__(self) -> Iterable:
        raise NotImplementedError

    def __contains__(self, key: str) -> bool:
        for cache in self.caches:
            if key in cache:
                return True
        return False
