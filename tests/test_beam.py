# tests/test_beam.py

from beam_py import Beam

def test_beam_creation():
    beam = Beam(length=10, load=500)
    assert beam.length == 10
    assert beam.load == 500

def test_calculate_reactions():
    beam = Beam(length=10, load=500)
    reactions = beam.calculate_reactions()
    assert isinstance(reactions, tuple)
    assert len(reactions) == 2
