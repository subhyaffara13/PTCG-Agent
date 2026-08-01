
def test_sympy__tensor__array__sparse_ndim_array__ImmutableSparseNDimArray():
    from sympy.tensor.array.sparse_ndim_array import ImmutableSparseNDimArray
    sparr = ImmutableSparseNDimArray(range(10, 34), (2, 3, 4))
    assert _test_args(sparr)

