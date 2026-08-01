
def test_integrate_series():
    f = sin(x).series(x, 0, 10)
    g = x**2/2 - x**4/24 + x**6/720 - x**8/40320 + x**10/3628800 + O(x**11)

    assert integrate(f, x) == g
    assert diff(integrate(f, x), x) == f

    assert integrate(O(x**5), x) == O(x**6)

