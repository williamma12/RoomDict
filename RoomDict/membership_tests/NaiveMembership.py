import logging

from RoomDict.membership_tests.GenericMembership import GenericMembership


class NaiveMembership(GenericMembership):
    def add(self, key: str):
        return

    def __contains__(self, key: str) -> bool:
        return False
