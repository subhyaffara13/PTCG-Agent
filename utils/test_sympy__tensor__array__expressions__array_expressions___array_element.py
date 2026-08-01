
def test_sympy__tensor__array__expressions__array_expressions__ArrayElement():
    from sympy.tensor.array.expressions.array_expressions import ArrayElement
    m, n, k = symbols("m n k")
    ae = ArrayElement("A", (m, n, k, 2))
    assert _test_args(ae)

