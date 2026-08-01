
def test_aliases():
    assert ln(7) == log(7)
    assert log10(3.75) == log(3.75,10)
    assert degrees(5.6) == 5.6 / degree
    assert radians(5.6) == 5.6 * degree
    assert power(-1,0.5) == j
    assert fmod(25,7) == 4.0 and isinstance(fmod(25,7), mpf)

