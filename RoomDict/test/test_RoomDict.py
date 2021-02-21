import pytest

from RoomDict.RoomDict import RoomDict

from RoomDict.test.utils import assert_equal


def test_naive_disk():
    key, value = ("TEST{}", "TSET{}")
    cache_policies = ["none"]
    membership_tests = ["none"]
    storage_backends = ["disk"]

    with RoomDict(cache_policies, membership_tests, storage_backends) as cache:
        for i in range(10):
            test_key = key.format(i)
            test_value = value.format(i)

            evicted = cache.__setitem__(test_key, test_value)
            actual_value = cache[test_key]

            assert_equal(test_value, actual_value)
            assert_equal(None, evicted)


def test_put_and_get_with_eviction():
    key, value = ("TEST{}", "TSET{}")
    cache_policies = ["lru"]
    cache_kwargs = [{"max_size": 5}]
    membership_tests = ["bloom"]
    membership_test_kwargs = [{"max_size": 10, "error_rate": 0.01}]
    storage_backends = ["memory"]

    with RoomDict(cache_policies, membership_tests, storage_backends, cache_kwargs, membership_test_kwargs) as cache:
        for i in range(10):
            test_key = key.format(i)
            test_value = value.format(i)

            evicted = cache.__setitem__(test_key, test_value)
            actual_value = cache[test_key]

            assert_equal(test_value, actual_value)

            if i < 5:
                assert_equal(None, evicted)
            else:
                expected_eviction = (key.format(i - 5), value.format(i - 5))
                assert_equal(expected_eviction, evicted)
