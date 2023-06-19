import unittest
from datetime import datetime
from unittest.mock import patch

from taximetro import Taximetro

class TestTaximetro(unittest.TestCase):

    def setUp(self):
        self.taximetro = Taximetro()

    def test_iniciar(self):
        self.assertFalse(self.taximetro.taximetroActivo)
        self.taximetro.iniciar()
        self.assertTrue(self.taximetro.taximetroActivo)
        self.assertEqual(self.taximetro.tarifaTotal, 0)

    def test_moverCoche(self):
        self.assertFalse(self.taximetro.cocheEnMovimiento)
        self.taximetro.taximetroActivo = True
        self.taximetro.moverCoche()
        self.assertTrue(self.taximetro.cocheEnMovimiento)
        self.assertEqual(self.taximetro.tarifaTotal, 0)

    def test_moverCoche_no_taximetro_activo(self):
        self.assertFalse(self.taximetro.cocheEnMovimiento)
        self.assertFalse(self.taximetro.taximetroActivo)
        self.taximetro.moverCoche()
        self.assertFalse(self.taximetro.cocheEnMovimiento)
        self.assertEqual(self.taximetro.tarifaTotal, 0)

    def test_detenerCoche(self):
        self.taximetro.cocheEnMovimiento = True
        self.taximetro.tiempoInicio = datetime.now()
        self.taximetro.detenerCoche()
        self.assertFalse(self.taximetro.cocheEnMovimiento)
        self.assertTrue(self.taximetro.yaSeAfrenado)

    def test_detenerCoche_no_coche_en_movimiento(self):
        self.assertFalse(self.taximetro.cocheEnMovimiento)
        self.taximetro.detenerCoche()
        self.assertFalse(self.taximetro.cocheEnMovimiento)
        self.assertFalse(self.taximetro.yaSeAfrenado)

    def test_finalizarRecorrido(self):
        self.taximetro.cocheEnMovimiento = False
        self.taximetro.taximetroActivo = True
        self.taximetro.finalizarRecorrido()
        self.assertFalse(self.taximetro.taximetroActivo)
        self.assertEqual(self.taximetro.tarifaTotal, 0)

    def test_finalizarRecorrido_no_taximetro_activo(self):
        self.assertFalse(self.taximetro.taximetroActivo)
        self.taximetro.finalizarRecorrido()
        self.assertFalse(self.taximetro.taximetroActivo)
        self.assertEqual(self.taximetro.tarifaTotal, 0)

    def test_calcularTarifa_detenido(self):
        with patch('time.time') as mock_time:
            mock_time.return_value = 0  # Mock the current time
            self.taximetro.tiempoInicio = 0
            self.taximetro.calcularTarifa("detenido")
            self.assertEqual(self.taximetro.tarifa, 0)
            self.assertEqual(self.taximetro.tarifaTotal, 0)

    def test_calcularTarifa_moviendose(self):
        with patch('time.time') as mock_time:
            mock_time.return_value = 0  # Mock the current time
            self.taximetro.tiempoInicio = 0
            self.taximetro.calcularTarifa("moviendose")
            self.assertEqual(self.taximetro.tarifa, 0)
            self.assertEqual(self.taximetro.tarifaTotal, 0)
        


