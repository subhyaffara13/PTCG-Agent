
def test_array_symbol():
    if not numpy:
        skip("numpy not installed.")
    a = ArraySymbol('a', (3,))
    f = lambdify((a), a)
    assert numpy.all(f(numpy.array([1,2,3])) == numpy.array([1,2,3]))

