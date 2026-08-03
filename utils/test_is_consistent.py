import time

def test_is_consistent():
    assert DimensionSystem((length, time)).is_consistent is True


def test_is_consistent():
    dimension_system = DimensionSystem([length, time])
    us = UnitSystem([m, s], dimension_system=dimension_system)
    assert us.is_consistent == True

