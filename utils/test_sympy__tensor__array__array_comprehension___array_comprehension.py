
def test_sympy__tensor__array__array_comprehension__ArrayComprehension():
    from sympy.tensor.array.array_comprehension import ArrayComprehension
    arrcom = ArrayComprehension(x, (x, 1, 5))
    assert _test_args(arrcom)

