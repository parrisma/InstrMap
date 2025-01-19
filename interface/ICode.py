from abc import ABC, abstractmethod
from src.CodeScheme import CodeScheme


class ICode(ABC):
    @abstractmethod
    def scheme(self) -> CodeScheme:
        pass

    @abstractmethod
    def value(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def gen_base_code_value() -> str:
        pass
