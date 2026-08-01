
def test_sympy__integrals__transforms__InverseHankelTransform():
    from sympy.integrals.transforms import InverseHankelTransform
    assert _test_args(InverseHankelTransform(2, x, y, 0))

