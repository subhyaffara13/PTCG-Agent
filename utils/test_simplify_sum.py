
def test_simplify_sum():
    y, t, v = symbols('y, t, v')

    _simplify = lambda e: simplify(e, doit=False)
    assert _simplify(Sum(x*y, (x, n, m), (y, a, k)) + \
        Sum(y, (x, n, m), (y, a, k))) == Sum(y * (x + 1), (x, n, m), (y, a, k))
    assert _simplify(Sum(x, (x, n, m)) + Sum(x, (x, m + 1, a))) == \
        Sum(x, (x, n, a))
    assert _simplify(Sum(x, (x, k + 1, a)) + Sum(x, (x, n, k))) == \
        Sum(x, (x, n, a))
    assert _simplify(Sum(x, (x, k + 1, a)) + Sum(x + 1, (x, n, k))) == \
        Sum(x, (x, n, a)) + Sum(1, (x, n, k))
    assert _simplify(Sum(x, (x, 0, 3)) * 3 + 3 * Sum(x, (x, 4, 6)) + \
        4 * Sum(z, (z, 0, 1))) == 4*Sum(z, (z, 0, 1)) + 3*Sum(x, (x, 0, 6))
    assert _simplify(3*Sum(x**2, (x, a, b)) + Sum(x, (x, a, b))) == \
        Sum(x*(3*x + 1), (x, a, b))
    assert _simplify(Sum(x**3, (x, n, k)) * 3 + 3 * Sum(x, (x, n, k)) + \
        4 * y * Sum(z, (z, n, k))) + 1 == \
            4*y*Sum(z, (z, n, k)) + 3*Sum(x**3 + x, (x, n, k)) + 1
    assert _simplify(Sum(x, (x, a, b)) + 1 + Sum(x, (x, b + 1, c))) == \
        1 + Sum(x, (x, a, c))
    assert _simplify(Sum(x, (t, a, b)) + Sum(y, (t, a, b)) + \
        Sum(x, (t, b+1, c))) == x * Sum(1, (t, a, c)) + y * Sum(1, (t, a, b))
    assert _simplify(Sum(x, (t, a, b)) + Sum(x, (t, b+1, c)) + \
        Sum(y, (t, a, b))) == x * Sum(1, (t, a, c)) + y * Sum(1, (t, a, b))
    assert _simplify(Sum(x, (t, a, b)) + 2 * Sum(x, (t, b+1, c))) == \
        _simplify(Sum(x, (t, a, b)) + Sum(x, (t, b+1, c)) + Sum(x, (t, b+1, c)))
    assert _simplify(Sum(x, (x, a, b))*Sum(x**2, (x, a, b))) == \
        Sum(x, (x, a, b)) * Sum(x**2, (x, a, b))
    assert _simplify(Sum(x, (t, a, b)) + Sum(y, (t, a, b)) + Sum(z, (t, a, b))) \
        == (x + y + z) * Sum(1, (t, a, b))          # issue 8596
    assert _simplify(Sum(x, (t, a, b)) + Sum(y, (t, a, b)) + Sum(z, (t, a, b)) + \
        Sum(v, (t, a, b))) == (x + y + z + v) * Sum(1, (t, a, b))  # issue 8596
    assert _simplify(Sum(x * y, (x, a, b)) / (3 * y)) == \
        (Sum(x, (x, a, b)) / 3)
    assert _simplify(Sum(f(x) * y * z, (x, a, b)) / (y * z)) \
        == Sum(f(x), (x, a, b))
    assert _simplify(Sum(c * x, (x, a, b)) - c * Sum(x, (x, a, b))) == 0
    assert _simplify(c * (Sum(x, (x, a, b))  + y)) == c * (y + Sum(x, (x, a, b)))
    assert _simplify(c * (Sum(x, (x, a, b)) + y * Sum(x, (x, a, b)))) == \
        c * (y + 1) * Sum(x, (x, a, b))
    assert _simplify(Sum(Sum(c * x, (x, a, b)), (y, a, b))) == \
                c * Sum(x, (x, a, b), (y, a, b))
    assert _simplify(Sum((3 + y) * Sum(c * x, (x, a, b)), (y, a, b))) == \
                c * Sum((3 + y), (y, a, b)) * Sum(x, (x, a, b))
    assert _simplify(Sum((3 + t) * Sum(c * t, (x, a, b)), (y, a, b))) == \
                c*t*(t + 3)*Sum(1, (x, a, b))*Sum(1, (y, a, b))
    assert _simplify(Sum(Sum(d * t, (x, a, b - 1)) + \
                Sum(d * t, (x, b, c)), (t, a, b))) == \
                    d * Sum(1, (x, a, c)) * Sum(t, (t, a, b))
    assert _simplify(Sum(sin(t)**2 + cos(t)**2 + 1, (t, a, b))) == \
        2 * Sum(1, (t, a, b))

