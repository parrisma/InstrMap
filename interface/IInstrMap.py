from typing import List
from interface.ICode import ICode
from interface.IAgent import IAgent
from src.CodeScheme import CodeScheme
from abc import ABC, abstractmethod


class IInstrumentMap(ABC):

    @abstractmethod
    def create_instr(self,
                     agent: IAgent) -> ICode:
        raise NotImplementedError

    @abstractmethod
    def add_instr_codes(self, code:
                        ICode,
                        codes: List[ICode],
                        agent: IAgent) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_instr_codes(self,
                        code: ICode,
                        agent: IAgent) -> List[ICode]:
        raise NotImplementedError

    @abstractmethod
    def get_instr_code_of_type(self,
                               code: ICode,
                               code_scheme: CodeScheme,
                               agent: IAgent) -> List[ICode]:
        raise NotImplementedError
