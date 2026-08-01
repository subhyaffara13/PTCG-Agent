
def test_simpleDE():
    # Tests just the first valid DE
    for DE in simpleDE(exp(x), x, f):
        assert DE == (-f(x) + Derivative(f(x), x), 1)
        break
    for DE in simpleDE(sin(x), x, f):
        assert DE == (f(x) + Derivative(f(x), x, x), 2)
        break
    for DE in simpleDE(log(1 + x), x, f):
        assert DE == ((x + 1)*Derivative(f(x), x, 2) + Derivative(f(x), x), 2)
        break
    for DE in simpleDE(asin(x), x, f):
        assert DE == (x*Derivative(f(x), x) + (x**2 - 1)*Derivative(f(x), x, x),
                      2)
        break
    for DE in simpleDE(exp(x)*sin(x), x, f):
        assert DE == (2*f(x) - 2*Derivative(f(x)) + Derivative(f(x), x, x), 2)
        break
    for DE in simpleDE(((1 + x)/(1 - x))**n, x, f):
        assert DE == (2*n*f(x) + (x**2 - 1)*Derivative(f(x), x), 1)
        break
    for DE in simpleDE(airyai(x), x, f):
        assert DE == (-x*f(x) + Derivative(f(x), x, x), 2)
        break

