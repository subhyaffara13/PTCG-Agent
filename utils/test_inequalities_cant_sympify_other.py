
def test_inequalities_cant_sympify_other():
    # see issue 7833
    from operator import gt, lt, ge, le

    bar = "foo"

    for a in (x, S.Zero, S.One/3, pi, I, zoo, oo, -oo, nan, Rational(1, 3)):
        for op in (lt, gt, le, ge):
            raises(TypeError, lambda: op(a, bar))

