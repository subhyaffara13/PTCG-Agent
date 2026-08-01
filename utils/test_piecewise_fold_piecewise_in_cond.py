
def test_piecewise_fold_piecewise_in_cond():
    p1 = Piecewise((cos(x), x < 0), (0, True))
    p2 = Piecewise((0, Eq(p1, 0)), (p1 / Abs(p1), True))
    assert p2.subs(x, -pi/2) == 0
    assert p2.subs(x, 1) == 0
    assert p2.subs(x, -pi/4) == 1
    p4 = Piecewise((0, Eq(p1, 0)), (1,True))
    ans = piecewise_fold(p4)
    for i in range(-1, 1):
        assert ans.subs(x, i) == p4.subs(x, i)

    r1 = 1 < Piecewise((1, x < 1), (3, True))
    ans = piecewise_fold(r1)
    for i in range(2):
        assert ans.subs(x, i) == r1.subs(x, i)

    p5 = Piecewise((1, x < 0), (3, True))
    p6 = Piecewise((1, x < 1), (3, True))
    p7 = Piecewise((1, p5 < p6), (0, True))
    ans = piecewise_fold(p7)
    for i in range(-1, 2):
        assert ans.subs(x, i) == p7.subs(x, i)

