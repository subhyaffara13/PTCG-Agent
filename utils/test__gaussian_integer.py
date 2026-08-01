
def test_GaussianInteger():
    assert str(ZZ_I(1, 0)) == "1"
    assert str(ZZ_I(-1, 0)) == "-1"
    assert str(ZZ_I(0, 1)) == "I"
    assert str(ZZ_I(0, -1)) == "-I"
    assert str(ZZ_I(0, 2)) == "2*I"
    assert str(ZZ_I(0, -2)) == "-2*I"
    assert str(ZZ_I(1, 1)) == "1 + I"
    assert str(ZZ_I(-1, -1)) == "-1 - I"
    assert str(ZZ_I(-1, -2)) == "-1 - 2*I"

