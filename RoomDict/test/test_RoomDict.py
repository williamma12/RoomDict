import pytest

from RoomDict.RoomDict import RoomDict

from RoomDict.test.utils import assert_equal

def test_put_and_get():
    cache = RoomDict()

    test_key, test_value = ("TEST", "TSET")

    with RoomDict(5) as cache:
        cache[test_key] = test_value

        actual_value = cache[test_key]

        assert_equal(test_value, actual_value)
