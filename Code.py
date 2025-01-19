from CodeScheme import CodeScheme
from guid import GUID
from dataclasses import dataclass


@dataclass(frozen=True)
class Code:
    """
    Represents a code where a code has both a value an a schemw, where scheme is the type of code.
    Attributes:
        code_scheme (CodeScheme): The scheme associated with the code.
        code_value (str): The value of the code.
    Methods:
        scheme() -> CodeScheme: Returns the code scheme.
        value() -> str: Returns the code value.
    Static Methods:
        gen_base_code_value() -> str: Generates a new globally unique base code.
    """
    code_scheme: CodeScheme
    code_value: str

    def __post_init__(self):
        if not isinstance(self.code_scheme, CodeScheme):
            raise ValueError(
                "Invalid code_scheme: must be an instance of CodeScheme")
        if not isinstance(self.code_value, str) or not self.code_value:
            raise ValueError(
                "Invalid code_value: must be a non-empty string")

    def scheme(self) -> CodeScheme:
        return self.code_scheme

    def value(self) -> str:
        return self.code_value

    @staticmethod
    def gen_base_code_value() -> str:
        return str(GUID())

    def __eq__(self, other) -> bool:
        if isinstance(other, Code):
            return self.code_scheme == other.code_scheme and self.code_value == other.code_value
        return False

    def __hash__(self) -> int:
        return hash((self.code_scheme, self.code_value))

    def __str__(self) -> str:
        return f"scheme: {self.code_scheme} : value: {self.code_value}"

    def __repr__(self) -> str:
        return self.__str__()
