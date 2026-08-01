
def test_sympy__integrals__transforms__FourierTransform():
    from sympy.integrals.transforms import FourierTransform
    assert _test_args(FourierTransform(2, x, y))

