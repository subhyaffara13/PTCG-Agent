
def test_sympy__printing__rust__float_floor():
    from sympy.printing.rust import float_floor
    assert _test_args(float_floor(x))

