from collections.abc import Iterable, MutableMapping
import os
import shelve
from typing import List, Optional, Union

from RoomDict.caches import LRUCache, InfCache
from RoomDict.membership_tests import BloomMembership, NaiveMembership
from RoomDict.storage_backends import DiskStorage, MemoryStorage

CACHE_POLICY_MAPPING = {
    "lru": LRUCache,
    "none": InfCache,
}
MEMBERSHIP_TEST_MAPPING = {
    "bloom": BloomMembership,
    "none": NaiveMembership,
}
STORAGE_BACKEND_MAPPING = {
    "memory": MemoryStorage,
    "disk": DiskStorage,
}


class RoomDict(MutableMapping):
    def __init__(
        self,
        cache_policies: List[str],
        membership_tests: List[str],
        storage_backends: List[str],
        cache_policies_kwargs: Optional[List[dict]] = None,
        membership_tests_kwargs: Optional[List[dict]] = None,
        storage_backends_kwargs: Optional[List[dict]] = None,
    ):
        """Initialize a RoomDict with the given storage_backends and cache_policies.

        Parameters
        ----------
        cache_policies : List[str]
            List of cache policy strings.
        membership_tests : List[str]
            List of membership test strings.
        storage_backends : List[str]
            List of storage backend strings. Order implies the storage hierarchy.
        cache_policies_kwargs: Optional[List[dict]]
            Dictionary of cache policies initialization kwargs.
        membership_tests_kwargs: Optional[List[dict]]
            Dictionary of membership tests initialization kwargs.
        storage_backends_kwargs : Optional[List[dict]]
            Dictionary of storage backend initialization kwargs.

        Returns
        -------
        RoomDict
            RoomDict with chosen parameters.
        """
        assert len(storage_backends) == len(
            cache_policies
        ), "Must have equal numbers of storage backends and cache policies."

        if cache_policies_kwargs is None:
            cache_policies_kwargs = []
        if membership_tests_kwargs is None:
            membership_tests_kwargs = []
        if storage_backends_kwargs is None:
            storage_backends_kwargs = []

        if len(cache_policies_kwargs) != len(cache_policies):
            cache_policies_kwargs += [{}] * (
                len(cache_policies) - len(cache_policies_kwargs)
            )
        if len(membership_tests_kwargs) != len(membership_tests):
            membership_tests_kwargs += [{}] * (
                len(membership_tests) - len(membership_tests_kwargs)
            )
        if len(storage_backends_kwargs) != len(storage_backends):
            storage_backends_kwargs += [{}] * (
                len(storage_backends) - len(storage_backends_kwargs)
            )

        self._initialize_cache_and_storage(
            cache_policies,
            membership_tests,
            storage_backends,
            cache_policies_kwargs,
            membership_tests_kwargs,
            storage_backends_kwargs,
        )

    def _initialize_cache_and_storage(
        self,
        cache_policies: List[str],
        membership_tests: List[str],
        storage_backends: List[str],
        cache_policies_kwargs: List[dict],
        membership_tests_kwargs: List[dict],
        storage_backends_kwargs: List[dict],
    ):
        self.caches = []
        self.storage_backends = []
        for cache_policy, membership_test, storage_backend, cache_kwargs, membership_test_kwargs, storage_kwargs in zip(
            cache_policies,
            membership_tests,
            storage_backends,
            cache_policies_kwargs,
            membership_tests_kwargs,
            storage_backends_kwargs,
        ):
            cache_policy = CACHE_POLICY_MAPPING[cache_policy]

            membership_test = MEMBERSHIP_TEST_MAPPING[membership_test]
            membership_test = membership_test(**membership_test_kwargs)

            storage_backend = STORAGE_BACKEND_MAPPING[storage_backend]
            storage_backend = storage_backend(**storage_kwargs)

            self.caches.append(cache_policy(membership_test, storage_backend, **cache_kwargs))
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

    def __setitem__(self, key: str, value: object):
        del self[key]

        evicted = (key, value)
        for cache in self.caches:
            evicted = cache.put(*evicted)
            if evicted is None:
                return None

        return evicted

    def __getitem__(self, key: str):
        value = None
        for cache in self.caches:
            if key in cache:
                value = cache.pop(key)

        # Move retrieved value to highest level cache.
        if value is None:
            return None
        else:
            self.__setitem__(key, value)
            return value

    def __delitem__(self, key: str):
        for cache in self.caches:
            if key in cache:
                del cache[key]

    def __iter__(self) -> Iterable:
        raise NotImplementedError

    def __contains__(self, key: str) -> bool:
        exists = False
        for cache in self.caches:
            if key in cache:
                exists = True
                break

        return exists
