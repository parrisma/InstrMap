from enum import Enum


class CodeScheme(Enum):
    BASE = (0, "BASE")
    SEDOL = (1, "SEDOL")
    ISIN = (2, "ISIN")
    RIC = (3, "RIC")

    def __init__(self, num, description) -> None:
        self.num = num
        self.description = description

    def __str__(self) -> str:
        return self.description

    def __repr__(self) -> str:
        return self.__str__()
