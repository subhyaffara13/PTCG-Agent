
def test_sympy__tensor__array__expressions__array_expressions__PermuteDims():
    from sympy.tensor.array.expressions.array_expressions import PermuteDims
    A = MatrixSymbol("A", 4, 4)
    assert _test_args(PermuteDims(A, (1, 0)))

