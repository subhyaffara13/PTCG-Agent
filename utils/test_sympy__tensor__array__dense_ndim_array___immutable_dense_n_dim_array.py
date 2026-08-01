
def test_sympy__tensor__array__dense_ndim_array__ImmutableDenseNDimArray():
    from sympy.tensor.array.dense_ndim_array import ImmutableDenseNDimArray
    densarr = ImmutableDenseNDimArray(range(10, 34), (2, 3, 4))
    assert _test_args(densarr)

