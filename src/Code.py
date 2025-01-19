from interface.ICode import ICode
from src.CodeScheme import CodeScheme
from src.GloballyUniqueIdentifier import GloballyUniqueIdentifier
from dataclasses import dataclass


@dataclass(frozen=True)
class Code(ICode):
    """
    Represents a code where a code has both a value and a scheme, where scheme is the type of code.
    Attributes:
        code_scheme (CodeScheme): The scheme associated with the code.
        code_value (str): The value of the code.
    Methods:
        scheme() -> CodeScheme: Returns the code scheme.
        value() -> str: Returns the code value.
    Static Methods:
        gen_base_code_value() -> str: Generates a new globally unique base code.
    """
    scheme: CodeScheme
    value: str

    def __post_init__(self):
        if not isinstance(self.scheme, CodeScheme):
            raise ValueError(
                "Invalid code_scheme: must be an instance of CodeScheme")
        if not isinstance(self.value, str) or not self.value:
            raise ValueError(
                "Invalid code_value: must be a non-empty string")

    def scheme(self) -> CodeScheme:
        return self.scheme

    def value(self) -> str:
        return self.value

    @staticmethod
    def gen_base_code_value() -> str:
        return str(GloballyUniqueIdentifier())

    def __str__(self) -> str:
        return f"scheme: {self.scheme} : value: {self.value}"
