
def test_hyperbolic():
    assert sinh(x).nseries(x, n=6) == x + x**3/6 + x**5/120 + O(x**6)
    assert cosh(x).nseries(x, n=5) == 1 + x**2/2 + x**4/24 + O(x**5)
    assert tanh(x).nseries(x, n=6) == x - x**3/3 + 2*x**5/15 + O(x**6)
    assert coth(x).nseries(x, n=6) == \
        1/x - x**3/45 + x/3 + 2*x**5/945 + O(x**6)
    assert asinh(x).nseries(x, n=6) == x - x**3/6 + 3*x**5/40 + O(x**6)
    assert acosh(x).nseries(x, n=6) == \
        pi*I/2 - I*x - 3*I*x**5/40 - I*x**3/6 + O(x**6)
    assert atanh(x).nseries(x, n=6) == x + x**3/3 + x**5/5 + O(x**6)
    assert acoth(x).nseries(x, n=6) == -I*pi/2 + x + x**3/3 + x**5/5 + O(x**6)


def test_hyperbolic():
    assert integrate(coth(x)) == x - log(tanh(x) + 1) + log(tanh(x))
    assert integrate(sech(x)) == 2*atan(tanh(x/2))
    assert integrate(csch(x)) == log(tanh(x/2))

