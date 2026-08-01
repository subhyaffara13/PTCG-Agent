
def test_guess_generating_function_rational():
    x = Symbol('x')
    assert guess_generating_function_rational([fibonacci(k)
        for k in range(5, 15)]) == ((3*x + 5)/(-x**2 - x + 1))

