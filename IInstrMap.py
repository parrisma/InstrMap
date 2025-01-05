from typing import List
from Code import Code
from CodeScheme import CodeScheme
from CodeDoesNotExist import CodeDoesNotExist
from abc import ABC, abstractmethod


class IInstrumentMap(ABC):

    @abstractmethod
    def create_instr(self) -> Code:
        raise NotImplementedError

    @abstractmethod
    def add_instr_codes(self, code: Code, codes: List[Code]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_instr_codes(self, code: Code) -> List[Code]:
        raise NotImplementedError
