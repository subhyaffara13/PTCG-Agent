
def test_sympy__tensor__array__expressions__array_expressions__ArraySymbol():
    from sympy.tensor.array.expressions.array_expressions import ArraySymbol
    m, n, k = symbols("m n k")
    array = ArraySymbol("A", (m, n, k, 2))
    assert _test_args(array)

