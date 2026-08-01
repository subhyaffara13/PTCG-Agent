
def test_sympy__integrals__transforms__InverseMellinTransform():
    from sympy.integrals.transforms import InverseMellinTransform
    assert _test_args(InverseMellinTransform(2, x, y, 0, 1))

