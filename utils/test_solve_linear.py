
def test_solve_linear():
    w = Wild('w')
    assert solve_linear(x, x) == (0, 1)
    assert solve_linear(x, exclude=[x]) == (0, 1)
    assert solve_linear(x, symbols=[w]) == (0, 1)
    assert solve_linear(x, y - 2*x) in [(x, y/3), (y, 3*x)]
    assert solve_linear(x, y - 2*x, exclude=[x]) == (y, 3*x)
    assert solve_linear(3*x - y, 0) in [(x, y/3), (y, 3*x)]
    assert solve_linear(3*x - y, 0, [x]) == (x, y/3)
    assert solve_linear(3*x - y, 0, [y]) == (y, 3*x)
    assert solve_linear(x**2/y, 1) == (y, x**2)
    assert solve_linear(w, x) in [(w, x), (x, w)]
    assert solve_linear(cos(x)**2 + sin(x)**2 + 2 + y) == \
        (y, -2 - cos(x)**2 - sin(x)**2)
    assert solve_linear(cos(x)**2 + sin(x)**2 + 2 + y, symbols=[x]) == (0, 1)
    assert solve_linear(Eq(x, 3)) == (x, 3)
    assert solve_linear(1/(1/x - 2)) == (0, 0)
    assert solve_linear((x + 1)*exp(-x), symbols=[x]) == (x, -1)
    assert solve_linear((x + 1)*exp(x), symbols=[x]) == ((x + 1)*exp(x), 1)
    assert solve_linear(x*exp(-x**2), symbols=[x]) == (x, 0)
    assert solve_linear(0**x - 1) == (0**x - 1, 1)
    assert solve_linear(1 + 1/(x - 1)) == (x, 0)
    eq = y*cos(x)**2 + y*sin(x)**2 - y  # = y*(1 - 1) = 0
    assert solve_linear(eq) == (0, 1)
    eq = cos(x)**2 + sin(x)**2  # = 1
    assert solve_linear(eq) == (0, 1)
    raises(ValueError, lambda: solve_linear(Eq(x, 3), 3))

