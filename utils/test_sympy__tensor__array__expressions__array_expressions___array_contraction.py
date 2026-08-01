
def test_sympy__tensor__array__expressions__array_expressions__ArrayContraction():
    from sympy.tensor.array.expressions.array_expressions import ArrayContraction
    from sympy.tensor.indexed import IndexedBase
    A = symbols("A", cls=IndexedBase)
    assert _test_args(ArrayContraction(A, (0, 1)))

