
def test_sympy__tensor__array__expressions__array_expressions__Reshape():
    from sympy.tensor.array.expressions.array_expressions import ArraySymbol, Reshape
    A = ArraySymbol("A", (4,))
    assert _test_args(Reshape(A, (2, 2)))

