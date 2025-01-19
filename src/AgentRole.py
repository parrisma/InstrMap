from enum import Enum


class AgentRole(Enum):
    READER = (0, "Reader")
    MAINTAINER = (1, "Maintainer")

    def __init__(self, num, description) -> None:
        self.num = num
        self.description = description

    def __str__(self) -> str:
        return self.description

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if isinstance(other, AgentRole):
            return self.num == other.num and self.description == other.description
        return False

    def __hash__(self) -> int:
        return hash((self.num, self.description))
