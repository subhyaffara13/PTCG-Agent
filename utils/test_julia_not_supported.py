
def test_julia_not_supported():
    with raises(NotImplementedError):
        julia_code(S.ComplexInfinity)

    f = Function('f')
    assert julia_code(f(x).diff(x), strict=False) == (
        "# Not supported in Julia:\n"
        "# Derivative\n"
        "Derivative(f(x), x)"
    )

