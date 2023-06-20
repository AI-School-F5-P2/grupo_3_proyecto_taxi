import pytest
from taximetro import Taximetro

def test_inicializar_taximetro():
    taximetro = Taximetro()
    assert not taximetro.iniciar
    taximetro.iniciar()
    assert taximetro.iniciar

def test_mover_coche_taximetro_inactivo():
    taximetro = Taximetro()
    taximetro.iniciar()
    with pytest.raises(RuntimeError):
        taximetro.moverCoche()

def test_mover_coche_coche_en_movimiento():
    taximetro = Taximetro()
    taximetro.iniciar()
    taximetro.moverCoche()
    with pytest.raises(RuntimeError):
        taximetro.moverCoche()
