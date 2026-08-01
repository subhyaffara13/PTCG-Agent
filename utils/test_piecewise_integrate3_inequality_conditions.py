
def test_piecewise_integrate3_inequality_conditions():
    from sympy.utilities.iterables import cartes
    lim = (x, 0, 5)
    # set below includes two pts below range, 2 pts in range,
    # 2 pts above range, and the boundaries
    N = (-2, -1, 0, 1, 2, 5, 6, 7)

    p = Piecewise((1, x > a), (2, x > b), (0, True))
    ans = p.integrate(lim)
    for i, j in cartes(N, repeat=2):
        reps = dict(zip((a, b), (i, j)))
        assert ans.subs(reps) == p.subs(reps).integrate(lim)
    assert ans.subs(a, 4).subs(b, 1) == 0 + 2*3 + 1

    p = Piecewise((1, x > a), (2, x < b), (0, True))
    ans = p.integrate(lim)
    for i, j in cartes(N, repeat=2):
        reps = dict(zip((a, b), (i, j)))
        assert ans.subs(reps) == p.subs(reps).integrate(lim)

