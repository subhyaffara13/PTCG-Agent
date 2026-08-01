
def test_sympy__integrals__transforms__CosineTransform():
    from sympy.integrals.transforms import CosineTransform
    assert _test_args(CosineTransform(2, x, y))

