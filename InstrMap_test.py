import unittest
from TestUtil import TestUtil
from InstrMap import InstrumentMap
from Code import Code
from CodeScheme import CodeScheme
from CodeDoesNotExist import CodeDoesNotExist
from OnlyBaseCodeDefined import OnlyBaseCodeDefined


class TestInstrumentMap(unittest.TestCase):

    def test_empty_map(self):
        instrMap = InstrumentMap()
        test_code = Code(CodeScheme.BASE, Code.gen_base_code_value())
        with self.assertRaises(CodeDoesNotExist):
            instrMap.get_instr_codes(test_code)

    def test_create_instr(self):
        instrMap = InstrumentMap()
        new_code = instrMap.create_instr()
        if new_code is None or not isinstance(new_code, Code) or new_code.code_scheme != CodeScheme.BASE:
            self.fail(
                "code must be an instance of Code, a BASE code and cannot be None")

    def test_create_and_get_instr(self):
        instrMap = InstrumentMap()
        new_code = instrMap.create_instr()
        if new_code is None or not isinstance(new_code, Code) or new_code.code_scheme != CodeScheme.BASE:
            self.fail(
                "code must be an instance of Code, a BASE code and cannot be None")
        expected_codes = instrMap.get_instr_codes(new_code)
        self.assertEqual(len(expected_codes), 1)
        self.assertEqual(expected_codes[0], new_code)

    def test_add_instr_codes_for_bad_code(self):
        instrMap = InstrumentMap()
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(None, [])
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(str("BadCodeTypeAsNotTypeCode"), [])

    def test_add_instr_codes_for_missing_code(self):
        instrMap = InstrumentMap()
        new_code = instrMap.create_instr()
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(new_code, None)

    def test_add_instr_codes_for_bad_alt_codes(self):
        instrMap = InstrumentMap()
        test_code = instrMap.create_instr()

        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(test_code, None)

        good_code = Code(CodeScheme.BASE, Code.gen_base_code_value())
        bad_code = str("BadCodeTypeAsNotTypeCode")
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(test_code, [good_code, bad_code])

    def test_add_instr_codes(self):
        instrMap = InstrumentMap()
        test_code = instrMap.create_instr()
        test_alt_codes = [Code(CodeScheme.ISIN, TestUtil.genISIN()),
                          Code(CodeScheme.SEDOL, TestUtil.genSEDOL()),
                          Code(CodeScheme.RIC, TestUtil.genRIC())]
        instrMap.add_instr_codes(test_code, test_alt_codes)

        # Check to see if we can get codes for any of the alt codes and the original base code
        codes_to_check = [test_code] + test_alt_codes
        for code_to_test in codes_to_check:
            codes = instrMap.get_instr_codes(code_to_test)
            self.assertEqual(len(codes), len(test_alt_codes)+1)
            for code in codes_to_check:
                self.assertEqual(code in codes, True)

    def test_add_duplicate_insert_instr_codes(self):
        instrMap = InstrumentMap()
        test_code = instrMap.create_instr()
        test_alt_codes = [Code(CodeScheme.ISIN, TestUtil.genISIN()),
                          Code(CodeScheme.SEDOL, TestUtil.genSEDOL()),
                          Code(CodeScheme.RIC, TestUtil.genRIC())]
        instrMap.add_instr_codes(test_code, test_alt_codes)
        instrMap.add_instr_codes(test_code, test_alt_codes)
        # Duplicate codes should not be added
        codes_to_check = [test_code] + test_alt_codes
        for code_to_test in codes_to_check:
            codes = instrMap.get_instr_codes(code_to_test)
            self.assertEqual(len(codes), len(test_alt_codes)+1)
            for code in codes_to_check:
                self.assertEqual(code in codes, True)

    def test_add_conflicting_instr_codes(self):
        instrMap = InstrumentMap()
        test_code = instrMap.create_instr()
        test_alt_codes = [Code(CodeScheme.ISIN, TestUtil.genISIN()),
                          Code(CodeScheme.SEDOL, TestUtil.genSEDOL()),
                          Code(CodeScheme.RIC, TestUtil.genRIC())]
        instrMap.add_instr_codes(test_code, test_alt_codes)
        new_test_code = instrMap.create_instr()
        with self.assertRaises(ValueError):
            instrMap.add_instr_codes(new_test_code, test_alt_codes)

    def test_add_many_instr_codes(self):
        instrMap = InstrumentMap()
        all_tests = []
        for _ in range(20):
            test_code = instrMap.create_instr()
            test_alt_codes = [Code(CodeScheme.ISIN, TestUtil.genISIN()),
                              Code(CodeScheme.SEDOL, TestUtil.genSEDOL()),
                              Code(CodeScheme.RIC, TestUtil.genRIC())]
            instrMap.add_instr_codes(test_code, test_alt_codes)
            all_tests.append([test_code] + test_alt_codes)

        for codes_to_check in all_tests:
            for code_to_test in codes_to_check:
                codes = instrMap.get_instr_codes(code_to_test)
                self.assertEqual(len(codes), len(test_alt_codes)+1)
                for code in codes_to_check:
                    self.assertEqual(code in codes, True)

    def test_get_instr_code_of_type_for_bad_code(self):
        instrMap = InstrumentMap()
        with self.assertRaises(ValueError):
            instrMap.get_instr_code_of_type(None, CodeScheme.ISIN)
        with self.assertRaises(ValueError):
            instrMap.get_instr_code_of_type(
                str("BadCodeTypeAsNotTypeCode"), CodeScheme.ISIN)
        test_code = instrMap.create_instr()
        test_code_not_added = Code(CodeScheme.BASE, Code.gen_base_code_value())
        with self.assertRaises(CodeDoesNotExist):
            instrMap.get_instr_code_of_type(
                test_code_not_added, CodeScheme.RIC)
        with self.assertRaises(OnlyBaseCodeDefined):
            instrMap.get_instr_code_of_type(
                test_code, CodeScheme.ISIN)
        expected_code = instrMap.get_instr_code_of_type(
            test_code, CodeScheme.BASE)
        self.assertEqual(expected_code, test_code)

    def test_get_instr_code_of_type(self):
        instrMap = InstrumentMap()
        all_tests = []
        for _ in range(20):
            test_code = instrMap.create_instr()
            test_alt_codes = [Code(CodeScheme.ISIN, TestUtil.genISIN()),
                              Code(CodeScheme.SEDOL, TestUtil.genSEDOL()),
                              Code(CodeScheme.RIC, TestUtil.genRIC())]
            instrMap.add_instr_codes(test_code, test_alt_codes)
            all_tests.append([test_code] + test_alt_codes)

        for codes_to_check in all_tests:
            for code_to_test in codes_to_check:
                codes = instrMap.get_instr_codes(code_to_test)
                for code in codes:
                    base_code = instrMap.get_instr_code_of_type(
                        code, CodeScheme.BASE)
                    self.assertEqual(isinstance(
                        base_code, Code), True, f"All codes must have a Base code {code}")
                    code_test = instrMap.get_instr_code_of_type(
                        base_code, code.scheme())
                    self.assertEqual(isinstance(code_test, Code), True)
                    self.assertEqual(code, code_test)
