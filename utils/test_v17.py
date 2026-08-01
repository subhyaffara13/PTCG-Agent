
def test_V17():
    r1 = integrate((diff(f(x), x)*g(x)
                   - f(x)*diff(g(x), x))/(f(x)**2 - g(x)**2), x)
    # integral not calculated
    assert simplify(r1 - (f(x) - g(x))/(f(x) + g(x))/2) == 0

