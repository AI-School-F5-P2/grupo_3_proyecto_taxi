import unittest
from taximetro import Taximetro

class TestTaximetro(unittest.TestCase):
    def setUp(self):
        self.taximetro = Taximetro()

    def test_iniciar(self):
        self.taximetro.taximetroActivo = True
        self.assertTrue(self.taximetro.taximetroActivo)

if __name__ == '__main__':
    unittest.main()