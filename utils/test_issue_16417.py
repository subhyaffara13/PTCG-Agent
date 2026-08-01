
def test_issue_16417():
    z = Symbol('z')
    assert unchanged(Piecewise, (1, Or(Eq(im(z), 0), Gt(re(z), 0))), (2, True))

    x = Symbol('x')
    assert unchanged(Piecewise, (S.Pi, re(x) < 0),
                 (0, Or(re(x) > 0, Ne(im(x), 0))),
                 (S.NaN, True))
    r = Symbol('r', real=True)
    p = Piecewise((S.Pi, re(r) < 0),
                 (0, Or(re(r) > 0, Ne(im(r), 0))),
                 (S.NaN, True))
    assert p == Piecewise((S.Pi, r < 0),
                 (0, r > 0),
                 (S.NaN, True), evaluate=False)
    # Does not work since imaginary != 0...
    #i = Symbol('i', imaginary=True)
    #p = Piecewise((S.Pi, re(i) < 0),
    #              (0, Or(re(i) > 0, Ne(im(i), 0))),
    #              (S.NaN, True))
    #assert p == Piecewise((0, Ne(im(i), 0)),
    #                      (S.NaN, True), evaluate=False)
    i = I*r
    p = Piecewise((S.Pi, re(i) < 0),
                  (0, Or(re(i) > 0, Ne(im(i), 0))),
                  (S.NaN, True))
    assert p == Piecewise((0, Ne(im(i), 0)),
                          (S.NaN, True), evaluate=False)
    assert p == Piecewise((0, Ne(r, 0)),
                          (S.NaN, True), evaluate=False)

