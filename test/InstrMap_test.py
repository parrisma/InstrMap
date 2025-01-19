import unittest
from TestUtil import TestUtil
from src.InstrMap import InstrumentMap
from exception.Code import Code
from src.CodeScheme import CodeScheme
from src.Agent import Agent
from src.AgentRole import AgentRole
from exception.CodeDoesNotExist import CodeDoesNotExist
from exception.OnlyBaseCodeDefined import OnlyBaseCodeDefined
from exception.IncorrectPermissions import IncorrectPermissions


class TestInstrumentMap(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.agent_maint = Agent(agent_id=Agent.gen_agent_id(),
                                agent_name="TestAgent",
                                agent_role=AgentRole.MAINTAINER)
        cls.agent_reader = Agent(agent_id=Agent.gen_agent_id(),
                                 agent_name="TestAgent",
                                 agent_role=AgentRole.READER)

    def test_empty_map(self):
        instrMap = InstrumentMap()
        test_code = Code(CodeScheme.BASE, Code.gen_base_code_value())
        with self.assertRaises(CodeDoesNotExist):
            instrMap.get_instr_codes(code=test_code, agent=self.agent_reader)

    def test_create_instr(self):
        instrMap = InstrumentMap()

        with self.assertRaises(ValueError):
            _ = instrMap.create_instr(agent=None)
        with self.assertRaises(ValueError):
            _ = instrMap.create_instr(agent=str("BadAgentTypeAsNotTypeAgent"))

        new_code = instrMap.create_instr(agent=self.agent_maint)
        if new_code is None or not isinstance(new_code, Code) or new_code.scheme != CodeScheme.BASE:
            self.fail(
                "code must be an instance of Code, a BASE code and cannot be None")

        with self.assertRaises(IncorrectPermissions):
            _ = instrMap.create_instr(agent=self.agent_reader)

    def test_create_and_get_instr(self):

        instrMap = InstrumentMap()
        with self.assertRaises(ValueError):
            _ = instrMap.create_instr(agent=None)
        with self.assertRaises(ValueError):
            _ = instrMap.create_instr(agent=str("BadAgentTypeAsNotTypeAgent"))

        new_code = instrMap.create_instr(agent=self.agent_maint)
        if new_code is None or not isinstance(new_code, Code) or new_code.scheme != CodeScheme.BASE:
            self.fail(
                "code must be an instance of Code, a BASE code and cannot be None")

        with self.assertRaises(ValueError):
            _ = instrMap.get_instr_codes(code=new_code, agent=None)
        with self.assertRaises(ValueError):
            _ = instrMap.get_instr_codes(
                code=new_code, agent=str("BadAgentTypeAsNotTypeAgent"))

        for test_agent in [self.agent_maint, self.agent_reader]:
            expected_codes = instrMap.get_instr_codes(
                code=new_code, agent=test_agent)
            self.assertEqual(len(expected_codes), 1)
            self.assertEqual(expected_codes[0], new_code)

    def test_add_instr_codes_for_bad_code(self):
        instrMap = InstrumentMap()
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(
                code=None, codes=[], agent=self.agent_maint)
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(
                code=str("BadCodeTypeAsNotTypeCode"), codes=[], agent=self.agent_maint)

    def test_add_instr_codes_for_missing_code(self):
        instrMap = InstrumentMap()
        new_code = instrMap.create_instr(agent=self.agent_maint)
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(
                code=new_code, codes=None, agent=self.agent_maint)

    def test_add_instr_codes_for_bad_alt_codes(self):
        instrMap = InstrumentMap()
        test_code = instrMap.create_instr(agent=self.agent_maint)

        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(
                code=test_code, codes=None, agent=self.agent_maint)

        good_code = Code(CodeScheme.BASE, Code.gen_base_code_value())
        bad_code = str("BadCodeTypeAsNotTypeCode")
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(code=test_code, codes=[
                                     good_code, bad_code], agent=self.agent_maint)

    def test_add_instr_codes(self):
        instrMap = InstrumentMap()
        test_code = instrMap.create_instr(agent=self.agent_maint)
        test_alt_codes = [Code(CodeScheme.ISIN, TestUtil.genISIN()),
                          Code(CodeScheme.SEDOL, TestUtil.genSEDOL()),
                          Code(CodeScheme.RIC, TestUtil.genRIC())]
        # Permission check
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(test_code, test_alt_codes, agent=None)
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(
                test_code, test_alt_codes, agent=str("BadAgentTypeAsNotTypeAgent"))
        with self.assertRaises(IncorrectPermissions):
            instrMap.add_instr_codes(
                test_code, test_alt_codes, agent=self.agent_reader)

        instrMap.add_instr_codes(
            test_code, test_alt_codes, agent=self.agent_maint)

        # Check to see if we can get codes for any of the alt codes and the original base code
        codes_to_check = [test_code] + test_alt_codes
        for code_to_test in codes_to_check:
            codes = instrMap.get_instr_codes(
                code=code_to_test, agent=self.agent_reader)
            self.assertEqual(len(codes), len(test_alt_codes)+1)
            for code in codes_to_check:
                self.assertEqual(code in codes, True)

    def test_add_duplicate_insert_instr_codes(self):
        instrMap = InstrumentMap()
        test_code = instrMap.create_instr(agent=self.agent_maint)
        test_alt_codes = [Code(CodeScheme.ISIN, TestUtil.genISIN()),
                          Code(CodeScheme.SEDOL, TestUtil.genSEDOL()),
                          Code(CodeScheme.RIC, TestUtil.genRIC())]
        instrMap.add_instr_codes(
            code=test_code, codes=test_alt_codes, agent=self.agent_maint)
        instrMap.add_instr_codes(
            code=test_code, codes=test_alt_codes, agent=self.agent_maint)
        # Duplicate codes should not be added
        codes_to_check = [test_code] + test_alt_codes
        for code_to_test in codes_to_check:
            codes = instrMap.get_instr_codes(
                code=code_to_test, agent=self.agent_reader)
            self.assertEqual(len(codes), len(test_alt_codes)+1)
            for code in codes_to_check:
                self.assertEqual(code in codes, True)

    def test_add_conflicting_instr_codes(self):
        instrMap = InstrumentMap()
        test_code = instrMap.create_instr(agent=self.agent_maint)
        test_alt_codes = [Code(CodeScheme.ISIN, TestUtil.genISIN()),
                          Code(CodeScheme.SEDOL, TestUtil.genSEDOL()),
                          Code(CodeScheme.RIC, TestUtil.genRIC())]
        instrMap.add_instr_codes(
            code=test_code, codes=test_alt_codes, agent=self.agent_maint)
        new_test_code = instrMap.create_instr(agent=self.agent_maint)
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(
                code=new_test_code, codes=test_alt_codes, agent=self.agent_maint)

    def test_add_many_instr_codes(self):
        instrMap = InstrumentMap()
        all_tests = []
        for _ in range(20):
            test_code = instrMap.create_instr(agent=self.agent_maint)
            test_alt_codes = [Code(CodeScheme.ISIN, TestUtil.genISIN()),
                              Code(CodeScheme.SEDOL, TestUtil.genSEDOL()),
                              Code(CodeScheme.RIC, TestUtil.genRIC())]
            instrMap.add_instr_codes(
                code=test_code, codes=test_alt_codes, agent=self.agent_maint)
            all_tests.append([test_code] + test_alt_codes)

        for codes_to_check in all_tests:
            for code_to_test in codes_to_check:
                codes = instrMap.get_instr_codes(
                    code=code_to_test, agent=self.agent_reader)
                self.assertEqual(len(codes), len(test_alt_codes)+1)
                for code in codes_to_check:
                    self.assertEqual(code in codes, True)

    def test_get_instr_code_of_type_for_bad_code(self):
        instrMap = InstrumentMap()
        dummy_but_valid_code = instrMap.create_instr(agent=self.agent_maint)

        with self.assertRaises(ValueError):
            instrMap.get_instr_code_of_type(
                code=None, code_scheme=CodeScheme.ISIN, agent=self.agent_reader)
        with self.assertRaises(ValueError):
            instrMap.get_instr_code_of_type(
                code=str("BadCodeTypeAsNotTypeCode"), code_scheme=CodeScheme.ISIN, agent=self.agent_reader)
        with self.assertRaises(ValueError):
            instrMap.get_instr_code_of_type(
                code=dummy_but_valid_code, code_scheme=CodeScheme.ISIN, agent=None)
        with self.assertRaises(ValueError):
            instrMap.get_instr_code_of_type(
                code=dummy_but_valid_code, code_scheme=CodeScheme.ISIN, agent=str("BadAgentTypeAsNotTypeAgent"))

        test_code = instrMap.create_instr(agent=self.agent_maint)
        test_code_not_added = Code(CodeScheme.BASE, Code.gen_base_code_value())
        with self.assertRaises(CodeDoesNotExist):
            instrMap.get_instr_code_of_type(
                code=test_code_not_added, code_scheme=CodeScheme.RIC, agent=self.agent_reader)
        with self.assertRaises(OnlyBaseCodeDefined):
            instrMap.get_instr_code_of_type(
                code=test_code, code_scheme=CodeScheme.ISIN, agent=self.agent_reader)
        expected_code = instrMap.get_instr_code_of_type(
            code=test_code, code_scheme=CodeScheme.BASE, agent=self.agent_reader)
        self.assertEqual(expected_code, test_code)

    def test_get_instr_code_of_type(self):
        instrMap = InstrumentMap()
        all_tests = []
        for _ in range(20):
            test_code = instrMap.create_instr(agent=self.agent_maint)
            test_alt_codes = [Code(CodeScheme.ISIN, TestUtil.genISIN()),
                              Code(CodeScheme.SEDOL, TestUtil.genSEDOL()),
                              Code(CodeScheme.RIC, TestUtil.genRIC())]
            instrMap.add_instr_codes(
                code=test_code, codes=test_alt_codes, agent=self.agent_maint)
            all_tests.append([test_code] + test_alt_codes)

        for codes_to_check in all_tests:
            for code_to_test in codes_to_check:
                codes = instrMap.get_instr_codes(
                    code=code_to_test, agent=self.agent_reader)
                for code in codes:
                    base_code = instrMap.get_instr_code_of_type(
                        code=code, code_scheme=CodeScheme.BASE, agent=self.agent_reader)
                    self.assertEqual(isinstance(
                        base_code, Code), True, f"All codes must have a Base code {code}")
                    code_test = instrMap.get_instr_code_of_type(
                        code=base_code, code_scheme=code.scheme, agent=self.agent_reader)
                    self.assertEqual(isinstance(code_test, Code), True)
                    self.assertEqual(code, code_test)
