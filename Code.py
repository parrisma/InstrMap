from typing import Tuple
from CodeScheme import CodeScheme
from guid import GUID


class Code:
    def __init__(self,
                 code_scheme: CodeScheme,
                 code_value: str) -> None:
        if not isinstance(code_scheme, CodeScheme):
            raise ValueError(
                "Invalid code_scheme: must be an instance of CodeScheme")
        if not isinstance(code_value, str) or not code_value:
            raise ValueError(
                "Invalid code_value: must be a non-empty string")
        self.code_scheme = code_scheme
        self.code_value = code_value
        return

    def scheme(self) -> Tuple[CodeScheme]:
        return (self.code_scheme)

    def value(self) -> Tuple[str]:
        return (self.code_value)

    @staticmethod
    def gen_base_code_value() -> Tuple[str]:
        return (str(GUID()))

    def __str__(self) -> str:
        return f"{self.code_scheme} : {self.code_value}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Code):
            return self.code_scheme == other.code_scheme and self.code_value == other.code_value
        return False

    def __hash__(self) -> int:
        return hash(f"{self.code_scheme}{self.code_value}")
