
def test_simplification():
    eq = x + (a - b)/(-2*a + 2*b)
    assert solveset(eq, x) == FiniteSet(S.Half)
    assert solveset(eq, x, S.Reals) == Intersection({-((a - b)/(-2*a + 2*b))}, S.Reals)
    # So that ap - bn is not zero:
    ap = Symbol('ap', positive=True)
    bn = Symbol('bn', negative=True)
    eq = x + (ap - bn)/(-2*ap + 2*bn)
    assert solveset(eq, x) == FiniteSet(S.Half)
    assert solveset(eq, x, S.Reals) == FiniteSet(S.Half)

