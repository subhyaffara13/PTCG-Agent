
def test_sympy__tensor__array__expressions__array_expressions__OneArray():
    from sympy.tensor.array.expressions.array_expressions import OneArray
    m, n, k = symbols("m n k")
    za = OneArray(m, n, k, 2)
    assert _test_args(za)

