
def test_octave_not_supported():
    with raises(NotImplementedError):
        mcode(S.ComplexInfinity)
    f = Function('f')
    assert mcode(f(x).diff(x), strict=False) == (
        "% Not supported in Octave:\n"
        "% Derivative\n"
        "Derivative(f(x), x)"
    )

