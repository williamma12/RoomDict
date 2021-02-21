import abc
from collections.abc import Container


class GenericMembership(Container):
    @abc.abstractmethod
    def add(self, key: str):
        pass

    @abc.abstractmethod
    def __contains__(self, key: str) -> bool:
        pass
