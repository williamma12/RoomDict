import logging

from pybloom import BloomFilter

from RoomDict.membership_tests.GenericMembership import GenericMembership


class BloomMembership(GenericMembership):
    def __init__(self, max_size: int, error_rate: float):
        self.bloom_filter = BloomFilter(max_size, error_rate)

    def add(self, key: str):
        self.bloom_filter.add(key)

    def __contains__(self, key: str) -> bool:
        return key in self.bloom_filter
