# importamos las librerias necesarias
import unittest
from datetime import datetime
from unittest.mock import patch

# importamos taximetro
from taximetro import Taximetro

# importar la clase a testear
class PruebaTesting(unittest.TestCase):
    
    # metodo para inicializar los parametros
    def initParam(self):
        # instanciar la clase
        self.taximetro = Taximetro();

    def primerTestValue(self):
        self.assertFalse(self.taximetro.taximetroActivo) # indica que el taximetro no esta activo
        self.taximetro.iniciar() # inicia el taximetro
        self.assertTrue(self.taximetro.taximetroActivo) # indica que el taximetro esta activo  
        self.assertEqual(self.taximetro.tarifaTotal, 0) # indica que la tarifa total es 0
        

    def segundoTestMov(self):
        self.assertFalse(self.taximetro.cocheEnMovimiento) # indica que el coche no esta en movimiento
        self.taximetro.taximetroActivo = True # indica que el taximetro esta activo
        self.assertTrue(self.taximetro.cocheEnMovimiento) # indica que el coche esta en movimiento
        self.assertEqual(self.taximetro.tarifaTotal, 0) # indica que la tarifa total es 0

    def tercerTestDet(self):
        self.taximetro.cocheEnMovimiento = True
        self.taximetro.taximetroActivo = True
        self.taximetro.detenerCoche()
        self.assertFalse(self.taximetro.cocheEnMovimiento) # indica que el coche no esta en movimiento
        self.assertEqual(self.taximetro.tarifaTotal, 0) # indica que la tarifa total es 0
        