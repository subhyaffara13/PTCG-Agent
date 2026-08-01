
def test_sympy__combinatorics__graycode__GrayCode():
    from sympy.combinatorics.graycode import GrayCode
    # an integer is given and returned from GrayCode as the arg
    assert _test_args(GrayCode(3, start='100'))
    assert _test_args(GrayCode(3, rank=1))

