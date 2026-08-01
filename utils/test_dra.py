
def test_dra():
    assert dra(19, 12) == 8
    assert dra(2718, 10) == 9
    assert dra(0, 22) == 0
    assert dra(23456789, 10) == 8
    raises(ValueError, lambda: dra(24, -2))
    raises(ValueError, lambda: dra(24.2, 5))

