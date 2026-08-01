
def test_leadterm():
    assert (3 + 2*x**(log(3)/log(2) - 1)).leadterm(x) == (3, 0)


def test_leadterm():
    assert (3 + 2*x**(log(3)/log(2) - 1)).leadterm(x) == (3, 0)

    assert (1/x**2 + 1 + x + x**2).leadterm(x)[1] == -2
    assert (1/x + 1 + x + x**2).leadterm(x)[1] == -1
    assert (x**2 + 1/x).leadterm(x)[1] == -1
    assert (1 + x**2).leadterm(x)[1] == 0
    assert (x + 1).leadterm(x)[1] == 0
    assert (x + x**2).leadterm(x)[1] == 1
    assert (x**2).leadterm(x)[1] == 2

