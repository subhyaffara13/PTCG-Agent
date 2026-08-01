
def test_fps__Add_expr():
    f = x*atan(x) - log(1 + x**2) / 2
    assert fps(f, x).truncate() == x**2/2 - x**4/12 + O(x**6)

    f = sin(x) + cos(x) - exp(x) + log(1 + x)
    assert fps(f, x).truncate() == x - 3*x**2/2 - x**4/4 + x**5/5 + O(x**6)

    f = 1/x + sin(x)
    assert fps(f, x).truncate() == 1/x + x - x**3/6 + x**5/120 + O(x**6)

    f = sin(x) - cos(x) + 1/(x - 1)
    assert fps(f, x).truncate() == \
        -2 - x**2/2 - 7*x**3/6 - 25*x**4/24 - 119*x**5/120 + O(x**6)

