import RoomDict.RoomDict as RoomDict

key, value = ("TEST{}", "TSET{}")
cache_policies = ["lru", "none"]
membership_tests = ["none", "none"]
storage_backends = ["memory", "arbitrary"]

cache_policies_kwargs = [{"max_size": 3}]
storage_backends_kwargs = [{}, {"delay": 100}]

with RoomDict(cache_policies, membership_tests, storage_backends, cache_policies_kwargs, storage_backends_kwargs=storage_backends_kwargs) as cache:
    for i in range(10):
        test_key = key.format(i)
        test_value = value.format(i)

        evicted = cache.__setitem__(test_key, test_value)
        actual_value = cache[test_key]
