
def test_complex_cast():
    """std::complex casts"""
    assert m.complex_cast(1) == "1.0"
    assert m.complex_cast(2j) == "(0.0, 2.0)"

