from typing import Iterator, Tuple

import pytest

from RoomDict.caches.LRUCache import LRUCache
from RoomDict.membership_tests import NaiveMembership
from RoomDict.membership_tests.GenericMembership import GenericMembership
from RoomDict.storage_backends import MemoryStorage
from RoomDict.storage_backends.GenericStorage import GenericStorage

from RoomDict.test.utils import assert_equal

TEST_SIZE = 5
TEST_RECORDS = [("test{}".format(i), i) for i in range(2 * TEST_SIZE)]
MEMBERSHIP_TEST = NaiveMembership
STORAGE_BACKEND = MemoryStorage


@pytest.fixture
def initialized_backends() -> Iterator[
    Tuple[GenericMembership, GenericStorage]
]:  # noqa: E501
    storage_backend = STORAGE_BACKEND()
    storage_backend.open()
    membership_test = MEMBERSHIP_TEST()

    yield (membership_test, storage_backend)

    storage_backend.close()


@pytest.fixture
def filled_cache(initialized_backends):
    membership_test, storage_backend = initialized_backends

    cache = LRUCache(membership_test, storage_backend, TEST_SIZE)

    for i in range(5):
        key, value = TEST_RECORDS[i]

        evicted_record = cache.put(key, value)
        expected_eviction = None

        assert_equal(expected_eviction, evicted_record)

    yield cache


def test_put(filled_cache):
    for i in range(5):
        key, value = TEST_RECORDS[i + TEST_SIZE]
        evicted_record = filled_cache.put(key, value)

        evicted_key, evicted_value = TEST_RECORDS[i]
        expected_eviction = (evicted_key, evicted_value)

        assert_equal(expected_eviction, evicted_record)


def test_get(filled_cache):
    for i in range(TEST_SIZE):
        key, value = TEST_RECORDS[i]

        actual_value = filled_cache.get(key)
        expected_value = value

        assert_equal(expected_value, actual_value)


def test_bad_get(filled_cache):
    actual_record = filled_cache.get("BAD_KEY")
    expected_record = None

    assert_equal(expected_record, actual_record)


def test_put_and_get(filled_cache):
    # Get first item to move it to most used.
    first_key, first_value = TEST_RECORDS[0]
    actual_first_value = filled_cache.get(first_key)
    assert_equal(first_value, actual_first_value)

    # Check that the second to last record is evicted.
    evicted_key, evicted_value = TEST_RECORDS[1]
    new_key, new_value = TEST_RECORDS[TEST_SIZE]

    expected_eviction = (evicted_key, evicted_value)
    actual_eviction = filled_cache.put(new_key, new_value)
    assert_equal(expected_eviction, actual_eviction)


def test_hot_key(filled_cache):
    hot_key, hot_value = TEST_RECORDS[0]

    for i in range(TEST_SIZE):
        evicted_key, evicted_value = TEST_RECORDS[i + 1]
        new_key, new_value = TEST_RECORDS[i + TEST_SIZE]

        actual_hot_value = filled_cache.get(hot_key)
        assert_equal(hot_value, actual_hot_value)

        expected_eviction = (evicted_key, evicted_value)
        actual_eviction = filled_cache.put(new_key, new_value)
        assert_equal(expected_eviction, actual_eviction)


def test_contains(filled_cache):
    for i in range(TEST_SIZE):
        cache_key, _ = TEST_RECORDS[i]
        assert cache_key in filled_cache


def test_deletion(filled_cache):
    for i in range(TEST_SIZE):
        cache_key, _ = TEST_RECORDS[i]
        del filled_cache[cache_key]


def test_not_contains(filled_cache):
    for i in range(TEST_SIZE):
        nonexistent_cache_key, _ = TEST_RECORDS[i + TEST_SIZE]
        assert nonexistent_cache_key not in filled_cache


@pytest.mark.xfail
def test_deletion_fail(filled_cache):
    for i in range(TEST_SIZE):
        nonexistent_cache_key, _ = TEST_RECORDS[i + TEST_SIZE]
        del filled_cache[nonexistent_cache_key]


def test_iter(filled_cache):
    cache_iterator = iter(filled_cache)
    for expected_record in TEST_RECORDS[:TEST_SIZE][::-1]:
        assert_equal(expected_record, next(cache_iterator))


@pytest.mark.xfail
def test_iter_empty(initialized_backends):
    membership_test, storage_backend = initialized_backends

    cache = LRUCache(membership_test, storage_backend, 1)
    cache_iterator = iter(cache)
    next(cache_iterator)
