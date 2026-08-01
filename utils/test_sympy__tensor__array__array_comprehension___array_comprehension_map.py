
def test_sympy__tensor__array__array_comprehension__ArrayComprehensionMap():
    from sympy.tensor.array.array_comprehension import ArrayComprehensionMap
    arrcomma = ArrayComprehensionMap(lambda: 0, (x, 1, 5))
    assert _test_args(arrcomma)

