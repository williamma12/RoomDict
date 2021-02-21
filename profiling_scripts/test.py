import RoomDict.RoomDict as RoomDict

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
