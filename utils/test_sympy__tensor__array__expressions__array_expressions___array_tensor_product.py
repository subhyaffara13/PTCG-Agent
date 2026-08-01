
def test_sympy__tensor__array__expressions__array_expressions__ArrayTensorProduct():
    from sympy.tensor.array.expressions.array_expressions import ArrayTensorProduct
    from sympy.tensor.indexed import IndexedBase
    A, B = symbols("A B", cls=IndexedBase)
    assert _test_args(ArrayTensorProduct(A, B))

