
def test_sympify():
    from sympy.abc import x, y, z, t
    arr = MutableDenseNDimArray([[x, y], [1, z*t]])
    arr_other = sympify(arr)
    assert arr_other.shape == (2, 2)
    assert arr_other == arr

