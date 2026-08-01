
def test_factorial_simplify():
    # There are more tests in test_factorials.py.
    x = Symbol('x')
    assert simplify(factorial(x)/x) == gamma(x)
    assert simplify(factorial(factorial(x))) == factorial(factorial(x))

