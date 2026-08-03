from typing import Tuple

def test_piecewise_integrate4_symbolic_conditions():
    a = Symbol('a', real=True)
    b = Symbol('b', real=True)
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    p0 = Piecewise((0, Or(x < a, x > b)), (1, True))
    p1 = Piecewise((0, x < a), (0, x > b), (1, True))
    p2 = Piecewise((0, x > b), (0, x < a), (1, True))
    p3 = Piecewise((0, x < a), (1, x < b), (0, True))
    p4 = Piecewise((0, x > b), (1, x > a), (0, True))
    p5 = Piecewise((1, And(a < x, x < b)), (0, True))

    # check values of a=1, b=3 (and reversed) with values
    # of y of 0, 1, 2, 3, 4
    lim = Tuple(x, -oo, y)
    for p in (p0, p1, p2, p3, p4, p5):
        ans = p.integrate(lim)
        for i in range(5):
            reps = {a:1, b:3, y:i}
            assert ans.subs(reps) == p.subs(reps).integrate(lim.subs(reps))
            reps = {a: 3, b:1, y:i}
            assert ans.subs(reps) == p.subs(reps).integrate(lim.subs(reps))
    lim = Tuple(x, y, oo)
    for p in (p0, p1, p2, p3, p4, p5):
        ans = p.integrate(lim)
        for i in range(5):
            reps = {a:1, b:3, y:i}
            assert ans.subs(reps) == p.subs(reps).integrate(lim.subs(reps))
            reps = {a:3, b:1, y:i}
            assert ans.subs(reps) == p.subs(reps).integrate(lim.subs(reps))

    ans = Piecewise(
        (0, x <= Min(a, b)),
        (x - Min(a, b), x <= b),
        (b - Min(a, b), True))
    for i in (p0, p1, p2, p4):
        assert i.integrate(x) == ans
    assert p3.integrate(x) == Piecewise(
        (0, x < a),
        (-a + x, x <= Max(a, b)),
        (-a + Max(a, b), True))
    assert p5.integrate(x) == Piecewise(
        (0, x <= a),
        (-a + x, x <= Max(a, b)),
        (-a + Max(a, b), True))

    p1 = Piecewise((0, x < a), (S.Half, x > b), (1, True))
    p2 = Piecewise((S.Half, x > b), (0, x < a), (1, True))
    p3 = Piecewise((0, x < a), (1, x < b), (S.Half, True))
    p4 = Piecewise((S.Half, x > b), (1, x > a), (0, True))
    p5 = Piecewise((1, And(a < x, x < b)), (S.Half, x > b), (0, True))

    # check values of a=1, b=3 (and reversed) with values
    # of y of 0, 1, 2, 3, 4
    lim = Tuple(x, -oo, y)
    for p in (p1, p2, p3, p4, p5):
        ans = p.integrate(lim)
        for i in range(5):
            reps = {a:1, b:3, y:i}
            assert ans.subs(reps) == p.subs(reps).integrate(lim.subs(reps))
            reps = {a: 3, b:1, y:i}
            assert ans.subs(reps) == p.subs(reps).integrate(lim.subs(reps))

