from typing import List
from Code import Code
from CodeScheme import CodeScheme
from Agent import Agent
from AgentRole import AgentRole
from CodeDoesNotExist import CodeDoesNotExist
from OnlyBaseCodeDefined import OnlyBaseCodeDefined
from IncorrectPermissions import IncorrectPermissions
from IInstrMap import IInstrumentMap


class InstrumentMap(IInstrumentMap):
    """
    InstrumentMap is a class that manages a map containing all code and the code schemes by which the code is known.

    In the map every case has a globally unquie base code and a list of related codes.

    Methods:
        create_instr() -> Code: Creates a new base instrument code and adds it to the map.
        add_instr_codes(code: Code, codes: List[Code]) -> None: Adds related codes to an existing base code.
        get_instr_codes(code: Code) -> List[Code]: Retrieves all related codes for a given code.
        get_instr_code_of_type(code: Code, code_scheme: CodeScheme) -> Code: Retrieves a specific type of code for a given code.
    """

    def __init__(self):
        super().__init__()
        self.instr_map = {}
        for scheme in CodeScheme:
            self.instr_map[str(scheme)] = {}
        return

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
        if agent is None or not isinstance(agent, Agent):
            raise ValueError(
                f"agent must be an instance of Agent and cannot be None: {agent}")

        if not agent.has_required_permissions(AgentRole.MAINTAINER):
            raise IncorrectPermissions(
                f"Agent {agent} does not have the required permissions to create an instrument)")

        new_code = Code(CodeScheme.BASE, Code.gen_base_code_value())
        self.instr_map[str(new_code.code_scheme)][new_code] = new_code
        return new_code

    def add_instr_codes(self,
                        code: Code,
                        codes: List[Code],
                        agent: Agent) -> None:
        """
        Adds a list of instrument codes to the instrument map for a given base code.
        Args:
            code (Code): The base code to which the instruction codes will be added.
            codes (List[Code]): A list of instrument codes to be added.
            agent (Agent): The agent requesting the addition of the alternate codes.
        Raises:
            ValueError: If any paramater is none or of the wrong type.
            ValueError: If an instrument code in `codes` already exists in the map with a different base code.
            CodeDoesNotExist: If the base `code` does not exist in the instrument map.
            IncorrectPermissions: If the agent does not have the required permissions to create an instrument.
        """
        if code is None or not isinstance(code, Code):
            raise ValueError(
                f"code must be an instance of Code and cannot be None: {code}")

        if code not in self.instr_map[str(code.code_scheme)]:
            raise CodeDoesNotExist(
                f"Cannot add codes for a Code that does not exist in the map: {code}")

        if codes is None:
            raise ValueError("codes cannot be None")

        if codes is not None:
            if not isinstance(codes, List) or not all(isinstance(code, Code) for code in codes):
                raise ValueError(
                    f"codes must be a list of Code instances, but got {type(codes)}")

        if agent is None or not isinstance(agent, Agent):
            raise ValueError(
                f"agent must be an instance of Agent and cannot be None: {agent}")

        if not agent.has_required_permissions(AgentRole.MAINTAINER):
            raise IncorrectPermissions(
                f"Agent {agent} does not have the required permissions {AgentRole.MAINTAINER} to create an instrument)")

        base_code = self.instr_map[str(code.code_scheme)][code]
        for c in codes:
            if c not in self.instr_map[str(c.code_scheme)]:
                self.instr_map[str(c.code_scheme)][c] = base_code
            else:
                curr_base = self.instr_map[str(c.code_scheme)][c]
                if curr_base != base_code:
                    raise ValueError(
                        f"Cannot add code for a Code that already exists in the map with a different base code: {c}")

    def get_instr_codes(self,
                        code: Code,
                        agent: Agent) -> List[Code]:
        """
        Retrieve all code schemes values that map to the given code
        Args:
            code (Code): The code for which to find all equivalent codes.
            agent (Agent): The agent requesting the get of the alternate codes.
        Returns:
            List[Code]: A list of codes that map to the same base code as the given code.
        Raises:
            ValueError: If the provided parameters are None or not an instance of required type.
            CodeDoesNotExist: If the provided code does not exist in the map.
            IncorrectPermissions: If the agent does not have the required permissions to create an instrument.
        """

        if code is None or not isinstance(code, Code):
            raise ValueError(
                f"code must be an instance of Code and cannot be None but got type {type(code)}")

        if code not in self.instr_map[str(code.code_scheme)]:
            raise CodeDoesNotExist(f"Code {code} does not exist in the map")

        if agent is None or not isinstance(agent, Agent):
            raise ValueError(
                f"agent must be an instance of Agent and cannot be None: {agent}")

        if not (agent.has_required_permissions(AgentRole.MAINTAINER) or agent.has_required_permissions(AgentRole.READER)):
            raise IncorrectPermissions(
                f"Agent {agent} does not have the required permissions {AgentRole.READER} to create an instrument)")

        base_code = self.instr_map[str(code.code_scheme)][code]

        all_codes = []
        for scheme in CodeScheme:
            codes = [key for key, value in self.instr_map[str(
                scheme)].items() if value == base_code]
            all_codes.extend(codes)

        return all_codes

    def get_instr_code_of_type(self,
                               code: Code,
                               code_scheme: CodeScheme,
                               agent: Agent) -> Code:
        """
        Retrieve the instruction code of a specific type from the instruction map.
        Args:
            code (Code): The code to search for. Must be an instance of Code and cannot be None.
            code_scheme (CodeScheme): The code scheme to match. Must be an instance of CodeScheme and cannot be None.
            agent (Agent): The agent requesting the get of the alternate codes.
        Returns:
            Code: The matching instruction code of the specified type.
        Raises:
            ValueError: If parameters are None or of the wrong type.
            CodeDoesNotExist: If the `code` does not exist in the instruction map.
            CodeDoesNotExist: If no matching code scheme is found for the given `code`.
            IncorrectPermissions: If the agent does not have the required permissions to create an instrument.
        """
        if code is None or not isinstance(code, Code):
            raise ValueError(
                "code must be an instance of Code and cannot be None")

        if code_scheme is None or not isinstance(code_scheme, CodeScheme):
            raise ValueError(
                "code sheme must be an instance of CodeScheme and cannot be None")

        if code not in self.instr_map[str(code.code_scheme)]:
            raise CodeDoesNotExist(f"Code {code} does not exist in the map")

        if agent is None or not isinstance(agent, Agent):
            raise ValueError(
                f"agent must be an instance of Agent and cannot be None: {agent}")

        if not (agent.has_required_permissions(AgentRole.MAINTAINER) or agent.has_required_permissions(AgentRole.READER)):
            raise IncorrectPermissions(
                f"Agent {agent} does not have the required permissions {AgentRole.READER} to create an instrument)")

        codes = self.get_instr_codes(code, agent=agent)

        for c in codes:
            if c.code_scheme == code_scheme:
                return c

        raise OnlyBaseCodeDefined(
            f"Code {code} has no matching codes for code scheme {code_scheme}")
