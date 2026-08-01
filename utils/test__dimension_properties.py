
def test_Dimension_properties():
    assert dimsys_SI.is_dimensionless(length) is False
    assert dimsys_SI.is_dimensionless(length/length) is True
    assert dimsys_SI.is_dimensionless(Dimension("undefined")) is False

    assert length.has_integer_powers(dimsys_SI) is True
    assert (length**(-1)).has_integer_powers(dimsys_SI) is True
    assert (length**1.5).has_integer_powers(dimsys_SI) is False

