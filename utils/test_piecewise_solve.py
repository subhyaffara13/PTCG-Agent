
def test_piecewise_solve():
    abs2 = Piecewise((-x, x <= 0), (x, x > 0))
    f = abs2.subs(x, x - 2)
    assert solve(f, x) == [2]
    assert solve(f - 1, x) == [1, 3]

    f = Piecewise(((x - 2)**2, x >= 0), (1, True))
    assert solve(f, x) == [2]

    g = Piecewise(((x - 5)**5, x >= 4), (f, True))
    assert solve(g, x) == [2, 5]

    g = Piecewise(((x - 5)**5, x >= 4), (f, x < 4))
    assert solve(g, x) == [2, 5]

    g = Piecewise(((x - 5)**5, x >= 2), (f, x < 2))
    assert solve(g, x) == [5]

    g = Piecewise(((x - 5)**5, x >= 2), (f, True))
    assert solve(g, x) == [5]

    g = Piecewise(((x - 5)**5, x >= 2), (f, True), (10, False))
    assert solve(g, x) == [5]

    g = Piecewise(((x - 5)**5, x >= 2),
                  (-x + 2, x - 2 <= 0), (x - 2, x - 2 > 0))
    assert solve(g, x) == [5]

    # if no symbol is given the piecewise detection must still work
    assert solve(Piecewise((x - 2, x > 2), (2 - x, True)) - 3) == [-1, 5]

    f = Piecewise(((x - 2)**2, x >= 0), (0, True))
    raises(NotImplementedError, lambda: solve(f, x))

    def nona(ans):
        return list(filter(lambda x: x is not S.NaN, ans))
    p = Piecewise((x**2 - 4, x < y), (x - 2, True))
    ans = solve(p, x)
    assert nona([i.subs(y, -2) for i in ans]) == [2]
    assert nona([i.subs(y, 2) for i in ans]) == [-2, 2]
    assert nona([i.subs(y, 3) for i in ans]) == [-2, 2]
    assert ans == [
        Piecewise((-2, y > -2), (S.NaN, True)),
        Piecewise((2, y <= 2), (S.NaN, True)),
        Piecewise((2, y > 2), (S.NaN, True))]

    # issue 6060
    absxm3 = Piecewise(
        (x - 3, 0 <= x - 3),
        (3 - x, 0 > x - 3)
    )
    assert solve(absxm3 - y, x) == [
        Piecewise((-y + 3, -y < 0), (S.NaN, True)),
        Piecewise((y + 3, y >= 0), (S.NaN, True))]
    p = Symbol('p', positive=True)
    assert solve(absxm3 - p, x) == [-p + 3, p + 3]

    # issue 6989
    f = Function('f')
    assert solve(Eq(-f(x), Piecewise((1, x > 0), (0, True))), f(x)) == \
        [Piecewise((-1, x > 0), (0, True))]

    # issue 8587
    f = Piecewise((2*x**2, And(0 < x, x < 1)), (2, True))
    assert solve(f - 1) == [1/sqrt(2)]

