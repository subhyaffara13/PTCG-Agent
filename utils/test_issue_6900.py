
def test_issue_6900():
    from itertools import permutations
    t0, t1, T, t = symbols('t0, t1 T t')
    f = Piecewise((0, t < t0), (x, And(t0 <= t, t < t1)), (0, t >= t1))
    g = f.integrate(t)
    assert g == Piecewise(
        (0, t <= t0),
        (t*x - t0*x, t <= Max(t0, t1)),
        (-t0*x + x*Max(t0, t1), True))
    for i in permutations(range(2)):
        reps = dict(zip((t0,t1), i))
        for tt in range(-1,3):
            assert (g.xreplace(reps).subs(t,tt) ==
                f.xreplace(reps).integrate(t).subs(t,tt))
    lim = Tuple(t, t0, T)
    g = f.integrate(lim)
    ans = Piecewise(
        (-t0*x + x*Min(T, Max(t0, t1)), T > t0),
        (0, True))
    for i in permutations(range(3)):
        reps = dict(zip((t0,t1,T), i))
        tru = f.xreplace(reps).integrate(lim.xreplace(reps))
        assert tru == ans.xreplace(reps)
    assert g == ans

