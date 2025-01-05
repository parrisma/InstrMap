from typing import List
from Code import Code
from CodeScheme import CodeScheme
from CodeDoesNotExist import CodeDoesNotExist


class InstrumentMap:

    def __init__(self):
        self.instr_map = {}
        for scheme in CodeScheme:
            self.instr_map[str(scheme)] = {}
        return

    def create_instr(self) -> Code:
        new_code = Code(CodeScheme.BASE, Code.gen_base_code_value())
        self.instr_map[str(new_code.code_scheme)][new_code] = new_code
        return new_code

    def add_instr_codes(self,
                        code: Code,
                        codes: List[Code]) -> None:
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
                    "codes must be a list of Code instances")

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
        if code is None or not isinstance(code, Code):
            raise ValueError(
                "code must be an instance of Code and cannot be None")

        if code not in self.instr_map[str(code.code_scheme)]:
            raise CodeDoesNotExist("Code does not exist in the map")

        base_code = self.instr_map[str(code.code_scheme)][code]

        all_codes = []
        for scheme in CodeScheme:
            codes = [key for key, value in self.instr_map[str(
                scheme)].items() if value == base_code]
            all_codes.extend(codes)

        return all_codes
