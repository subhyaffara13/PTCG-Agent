
def test_issue_24368():
    # Ideally these would produce a solution, but for now just check that they
    # don't fail with a RuntimeError
    raises(NotImplementedError, lambda: solve(Mod(x**2, 49), x))
    s2 = Symbol('s2', integer=True, positive=True)
    f = floor(s2/2 - S(1)/2)
    raises(NotImplementedError, lambda: solve((Mod(f**2/(f + 1) + 2*f/(f + 1) + 1/(f + 1), 1))*f + Mod(f**2/(f + 1) + 2*f/(f + 1) + 1/(f + 1), 1), s2))

