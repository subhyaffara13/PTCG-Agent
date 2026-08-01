
def test_issue_8919():
    c = symbols('c:5')
    x = symbols("x")
    f1 = Piecewise((c[1], x < 1), (c[2], True))
    f2 = Piecewise((c[3], x < Rational(1, 3)), (c[4], True))
    assert integrate(f1*f2, (x, 0, 2)
        ) == c[1]*c[3]/3 + 2*c[1]*c[4]/3 + c[2]*c[4]
    f1 = Piecewise((0, x < 1), (2, True))
    f2 = Piecewise((3, x < 2), (0, True))
    assert integrate(f1*f2, (x, 0, 3)) == 6

    y = symbols("y", positive=True)
    a, b, c, x, z = symbols("a,b,c,x,z", real=True)
    I = Integral(Piecewise(
        (0, (x >= y) | (x < 0) | (b > c)),
        (a, True)), (x, 0, z))
    ans = I.doit()
    assert ans == Piecewise((0, b > c), (a*Min(y, z) - a*Min(0, z), True))
    for cond in (True, False):
        for yy in range(1, 3):
            for zz in range(-yy, 0, yy):
                reps = [(b > c, cond), (y, yy), (z, zz)]
                assert ans.subs(reps) == I.subs(reps).doit()

