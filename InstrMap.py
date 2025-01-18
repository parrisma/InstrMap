from typing import List
from Code import Code
from CodeScheme import CodeScheme
from CodeDoesNotExist import CodeDoesNotExist
from OnlyBaseCodeDefined import OnlyBaseCodeDefined
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

    def create_instr(self) -> Code:
        """
        Creates a new unquie code with a base id and adds it to the instrument map.

        Returns:
            Code: The newly created instrument code.
        """
        new_code = Code(CodeScheme.BASE, Code.gen_base_code_value())
        self.instr_map[str(new_code.code_scheme)][new_code] = new_code
        return new_code

    def add_instr_codes(self,
                        code: Code,
                        codes: List[Code]) -> None:
        """
        Adds a list of instrument codes to the instrument map for a given base code.
        Args:
            code (Code): The base code to which the instruction codes will be added.
            codes (List[Code]): A list of instrument codes to be added.
        Raises:
            ValueError: If `code` is None or not an instance of `Code`.
            ValueError: If `codes` is not a list of `Code` instances.
            ValueError: If an instrument code in `codes` already exists in the map with a different base code.
            CodeDoesNotExist: If the base `code` does not exist in the instrument map.
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
                        code: Code) -> List[Code]:
        """
        Retrieve all code schemes values that map to the given code
        Args:
            code (Code): The code for which to find all equivalent codes.
        Returns:
            List[Code]: A list of codes that map to the same base code as the given code.
        Raises:
            ValueError: If the provided code is None or not an instance of Code.
            CodeDoesNotExist: If the provided code does not exist in the map.
        """

        if code is None or not isinstance(code, Code):
            raise ValueError(
                f"code must be an instance of Code and cannot be None but got type {type(code)}")

        if code not in self.instr_map[str(code.code_scheme)]:
            raise CodeDoesNotExist(f"Code {code} does not exist in the map")

        base_code = self.instr_map[str(code.code_scheme)][code]

        all_codes = []
        for scheme in CodeScheme:
            codes = [key for key, value in self.instr_map[str(
                scheme)].items() if value == base_code]
            all_codes.extend(codes)

        return all_codes

    def get_instr_code_of_type(self,
                               code: Code,
                               code_scheme: CodeScheme) -> Code:
        """
        Retrieve the instruction code of a specific type from the instruction map.
        Args:
            code (Code): The code to search for. Must be an instance of Code and cannot be None.
            code_scheme (CodeScheme): The code scheme to match. Must be an instance of CodeScheme and cannot be None.
        Returns:
            Code: The matching instruction code of the specified type.
        Raises:
            ValueError: If `code` is not an instance of Code or is None.
            ValueError: If `code_scheme` is not an instance of CodeScheme or is None.
            CodeDoesNotExist: If the `code` does not exist in the instruction map.
            CodeDoesNotExist: If no matching code scheme is found for the given `code`.
        """
        if code is None or not isinstance(code, Code):
            raise ValueError(
                "code must be an instance of Code and cannot be None")

        if code_scheme is None or not isinstance(code_scheme, CodeScheme):
            raise ValueError(
                "code sheme must be an instance of CodeScheme and cannot be None")

        if code not in self.instr_map[str(code.code_scheme)]:
            raise CodeDoesNotExist(f"Code {code} does not exist in the map")

        codes = self.get_instr_codes(code)

        for c in codes:
            if c.code_scheme == code_scheme:
                return c

        raise OnlyBaseCodeDefined(
            f"Code {code} has no matching codes for code scheme {code_scheme}")
