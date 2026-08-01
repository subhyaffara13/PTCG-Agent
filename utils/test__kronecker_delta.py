
def test_KroneckerDelta():
    from sympy.functions import KroneckerDelta
    assert mcode(KroneckerDelta(x, y)) == "double(x == y)"
    assert mcode(KroneckerDelta(x, y + 1)) == "double(x == (y + 1))"
    assert mcode(KroneckerDelta(2**x, y)) == "double((2.^x) == y)"

