
def test_sympy__matrices__expressions__fourier__DFT():
    from sympy.matrices.expressions.fourier import DFT
    from sympy.core.singleton import S
    assert _test_args(DFT(S(2)))

