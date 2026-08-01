
def test_array2matrix():
    # See issue https://github.com/sympy/sympy/pull/22877
    expr = PermuteDims(ArrayContraction(ArrayTensorProduct(x, I, I1, x), (0, 3), (1, 7)), Permutation(2, 3))
    expected = PermuteDims(ArrayTensorProduct(x*x.T, I1), Permutation(3)(1, 2))
    assert _array2matrix(expr) == expected

