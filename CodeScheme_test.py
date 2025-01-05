import unittest
from CodeScheme import CodeScheme

class TestCodeScheme(unittest.TestCase):

    def test_enum_values(self):
        self.assertEqual(CodeScheme.BASE.num, 0)
        self.assertEqual(CodeScheme.BASE.description, "BASE")
        self.assertEqual(CodeScheme.SEDOL.num, 1)
        self.assertEqual(CodeScheme.SEDOL.description, "SEDOL")
        self.assertEqual(CodeScheme.ISIN.num, 2)
        self.assertEqual(CodeScheme.ISIN.description, "ISIN")
        self.assertEqual(CodeScheme.RIC.num, 3)
        self.assertEqual(CodeScheme.RIC.description, "RIC")

    def test_str_method(self):
        self.assertEqual(str(CodeScheme.BASE), "BASE")
        self.assertEqual(str(CodeScheme.SEDOL), "SEDOL")
        self.assertEqual(str(CodeScheme.ISIN), "ISIN")
        self.assertEqual(str(CodeScheme.RIC), "RIC")

if __name__ == '__main__':
    unittest.main()
    
    