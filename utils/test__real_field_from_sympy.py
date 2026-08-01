
def test_RealField_from_sympy():
    assert RR.convert(S.Zero) == RR.dtype(0)
    assert RR.convert(S(0.0)) == RR.dtype(0.0)
    assert RR.convert(S.One) == RR.dtype(1)
    assert RR.convert(S(1.0)) == RR.dtype(1.0)
    assert RR.convert(sin(1)) == RR.dtype(sin(1).evalf())

