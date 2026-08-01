
def test_fps__asymptotic():
    f = exp(x)
    assert fps(f, x, oo) == f
    assert fps(f, x, -oo).truncate() == O(1/x**6, (x, oo))

    f = erf(x)
    assert fps(f, x, oo).truncate() == 1 + O(1/x**6, (x, oo))
    assert fps(f, x, -oo).truncate() == -1 + O(1/x**6, (x, oo))

    f = atan(x)
    assert fps(f, x, oo, full=True).truncate() == \
        -1/(5*x**5) + 1/(3*x**3) - 1/x + pi/2 + O(1/x**6, (x, oo))
    assert fps(f, x, -oo, full=True).truncate() == \
        -1/(5*x**5) + 1/(3*x**3) - 1/x - pi/2 + O(1/x**6, (x, oo))

    f = log(1 + x)
    assert fps(f, x, oo) != \
        (-1/(5*x**5) - 1/(4*x**4) + 1/(3*x**3) - 1/(2*x**2) + 1/x - log(1/x) +
         O(1/x**6, (x, oo)))
    assert fps(f, x, -oo) != \
        (-1/(5*x**5) - 1/(4*x**4) + 1/(3*x**3) - 1/(2*x**2) + 1/x + I*pi -
         log(-1/x) + O(1/x**6, (x, oo)))

