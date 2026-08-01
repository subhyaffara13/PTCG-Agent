
def test_sympy__integrals__transforms__InverseFourierTransform():
    from sympy.integrals.transforms import InverseFourierTransform
    assert _test_args(InverseFourierTransform(2, x, y))

