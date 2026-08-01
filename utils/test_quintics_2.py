
def test_quintics_2():
    f = x**5 + 15*x + 12
    s = solve(f, check=False)
    for r in s:
        res = f.subs(x, r.n()).n()
        assert tn(res, 0)

    f = x**5 - 15*x**3 - 5*x**2 + 10*x + 20
    s = solve(f)
    for r in s:
        assert r.func == CRootOf

    assert solve(x**5 - 6*x**3 - 6*x**2 + x - 6) == [
        CRootOf(x**5 - 6*x**3 - 6*x**2 + x - 6, 0),
        CRootOf(x**5 - 6*x**3 - 6*x**2 + x - 6, 1),
        CRootOf(x**5 - 6*x**3 - 6*x**2 + x - 6, 2),
        CRootOf(x**5 - 6*x**3 - 6*x**2 + x - 6, 3),
        CRootOf(x**5 - 6*x**3 - 6*x**2 + x - 6, 4)]

