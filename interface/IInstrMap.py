from typing import List
from exception.Code import Code
from src.CodeScheme import CodeScheme
from src.Agent import Agent
from abc import ABC, abstractmethod


class IInstrumentMap(ABC):

    @abstractmethod
    def create_instr(self,
                     agent: Agent) -> Code:
        """
        Creates an instrument record in the Instrument Map and allocates it a new globally unique identifier.

        Args:
            agent (Agent): The agent requesting the creation of the instrument.

        Raises:
            IncorrectPermissions: If the agent does not have the required permissions to create an instrument.
            ValueError: If given arguments are null or of the wrong type.
            
        Returns:
            Code: The created instrument object.
        """
        raise NotImplementedError

    @abstractmethod
    def add_instr_codes(self, code:
                        Code,
                        codes: List[Code],
                        agent: Agent) -> None:
        """
        Adds a the given list of alternate instrument codes to the given instrument. If a code is already associoated with
        instrument it is ignored.

        Args:
            code (Code): The instrument to add the alternate codes to.
            codes (List[Code]): The list of alternate codes to associate with the given instrument.
            agent (Agent): The agent requesting the addition of the alternate codes.

        Raises:
            CodeDoesNotExist: If the given code is no known in the instrument map.
            ValueError: If given arguments are null or of the wrong type.
            IncorrectPermissions: If the agent does not have the required permissions to add alternate codes to an instrument.
        """
        raise NotImplementedError

    @abstractmethod
    def get_instr_codes(self,
                        code: Code,
                        agent: Agent) -> List[Code]:
        """
        Gets the given list of alternate instrument codes for the given instrument, this list includes the given instrument.

        Args:
            code (Code): The instrument to get the alternate codes for.
            agent (Agent): The agent requesting the alternate codes.

        Raises:
            CodeDoesNotExist: If the given code is no known in the instrument map.
            ValueError: If given code is null or not an instance of Code.
            IncorrectPermissions: If the agent does not have the required permissions to get the alternate codes of an instrument.
        """
        raise NotImplementedError

    @abstractmethod
    def get_instr_code_of_type(self,
                               code: Code,
                               code_scheme: CodeScheme,
                               agent: Agent) -> List[Code]:
        """
        Gets the given code scheme of the given instrument.

        Args:
            code (Code): The instrument to get the alternate code for.
            code_scheme (CodeScheme): The code scheme to get the code for.
            agent (Agent): The agent requesting the alternate code.

        Raises:
            CodeDoesNotExist: If the given code is no known in the instrument map.
            ValueError: If given code is null or not an instance of Code.
            IncorrectPermissions: If the agent does not have the required permissions to get the alternate code of an instrument.
        """
        raise NotImplementedError
