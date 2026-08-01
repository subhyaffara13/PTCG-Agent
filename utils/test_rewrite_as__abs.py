
def test_rewrite_as_Abs():
    from itertools import permutations
    from sympy.functions.elementary.complexes import Abs
    from sympy.abc import x, y, z, w
    def test(e):
        free = e.free_symbols
        a = e.rewrite(Abs)
        assert not a.has(Min, Max)
        for i in permutations(range(len(free))):
            reps = dict(zip(free, i))
            assert a.xreplace(reps) == e.xreplace(reps)
    test(Min(x, y))
    test(Max(x, y))
    test(Min(x, y, z))
    test(Min(Max(w, x), Max(y, z)))

