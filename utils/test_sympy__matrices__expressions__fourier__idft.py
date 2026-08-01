
def test_sympy__matrices__expressions__fourier__IDFT():
    from sympy.matrices.expressions.fourier import IDFT
    from sympy.core.singleton import S
    assert _test_args(IDFT(S(2)))

