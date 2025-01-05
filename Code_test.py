import unittest
import uuid
from Code import Code
from CodeScheme import CodeScheme


class TestCode(unittest.TestCase):

    def setUp(self):
        self.scheme = CodeScheme.SEDOL
        self.code_value = "12345"
        self.code = Code(self.scheme, self.code_value)

    def test_init_valid(self):
        self.assertEqual(self.code.code_scheme, self.scheme)
        self.assertEqual(self.code.code_value, self.code_value)

    def test_init_invalid_scheme(self):
        with self.assertRaises(ValueError):
            Code("InvalidScheme", self.code_value)

    def test_init_invalid_value(self):
        with self.assertRaises(ValueError):
            Code(self.scheme, "")

    def test_scheme(self):
        self.assertEqual(self.code.scheme(), self.scheme)

    def test_value(self):
        self.assertEqual(self.code.value(), self.code_value)

    def test_gen_base_code_value(self):
        base_code_value = Code.gen_base_code_value()
        try:
            _ = uuid.UUID(base_code_value)  # Check if it is a valid UUID
            self.assertTrue(True)
        except ValueError:
            self.fail("gen_base_code_value() did not return a valid UUID")

    def test_str(self):
        self.assertEqual(str(self.code), f"{str(self.scheme)} : {self.code_value}")

    def test_eq(self):
        other_code = Code(self.scheme, self.code_value)
        self.assertTrue(self.code == other_code)

    def test_not_eq(self):
        other_code = Code(self.scheme, str(uuid.uuid4()))
        self.assertFalse(self.code == other_code)

    def test_hash(self):
        self.assertEqual(hash(self.code), hash(
            f"{str(self.scheme)}{self.code_value}"))


if __name__ == '__main__':
    unittest.main()
