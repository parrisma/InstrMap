from typing import List
from Code import Code
from CodeScheme import CodeScheme
from abc import ABC, abstractmethod


class IInstrumentMap(ABC):

    @abstractmethod
    def create_instr(self) -> Code:
        """
        Creates an instrument record in the Instrument Map and allocates it a new globally unique identifier.

        Returns:
            Code: The created instrument object.
        """
        raise NotImplementedError

    @abstractmethod
    def add_instr_codes(self, code: Code, codes: List[Code]) -> None:
        """
        Adds a the given list of alternate instrument codes to the given instrument. If a code is already associoated with
        instrument it is ignored.

        Args:
            code (Code): The instrument to add the alternate codes to.
            codes (List[Code]): The list of alternate codes to associate with the given instrument.

        Raises:
            CodeDoesNotExist: If the given code is no known in the instrument map.
            ValueError: If given arguments are null or of the wrong type.
        """
        raise NotImplementedError

    @abstractmethod
    def get_instr_codes(self, code: Code) -> List[Code]:
        """
        Gets the given list of alternate instrument codes for the given instrument, this list includes the given instrument.

        Args:
            code (Code): The instrument to get the alternate codes for.

        Raises:
            CodeDoesNotExist: If the given code is no known in the instrument map.
            ValueError: If given code is null or not an instance of Code.
        """
        raise NotImplementedError

    @abstractmethod
    def get_instr_code_of_type(self,
                               code: Code,
                               code_scheme: CodeScheme) -> List[Code]:
        """
        Gets the given code scheme of the given instrument.

        Args:
            code (Code): The instrument to get the alternate code for.
            code_scheme (CodeScheme): The code scheme to get the code for.

        Raises:
            CodeDoesNotExist: If the given code is no known in the instrument map.
            ValueError: If given code is null or not an instance of Code.
        """
        raise NotImplementedError
