
def test_collect_func():
    f = ((x + a + 1)**3).expand()

    assert collect(f, x) == a**3 + 3*a**2 + 3*a + x**3 + x**2*(3*a + 3) + \
        x*(3*a**2 + 6*a + 3) + 1
    assert collect(f, x, factor) == x**3 + 3*x**2*(a + 1) + 3*x*(a + 1)**2 + \
        (a + 1)**3

    assert collect(f, x, evaluate=False) == {
        S.One: a**3 + 3*a**2 + 3*a + 1,
        x: 3*a**2 + 6*a + 3, x**2: 3*a + 3,
        x**3: 1
    }

    assert collect(f, x, factor, evaluate=False) == {
        S.One: (a + 1)**3, x: 3*(a + 1)**2,
        x**2: umul(S(3), a + 1), x**3: 1}

