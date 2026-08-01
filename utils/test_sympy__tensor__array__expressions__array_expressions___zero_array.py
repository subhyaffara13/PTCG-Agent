
def test_sympy__tensor__array__expressions__array_expressions__ZeroArray():
    from sympy.tensor.array.expressions.array_expressions import ZeroArray
    m, n, k = symbols("m n k")
    za = ZeroArray(m, n, k, 2)
    assert _test_args(za)

