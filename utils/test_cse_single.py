
def test_cse_single():
    # Simple substitution.
    e = Add(Pow(x + y, 2), sqrt(x + y))
    substs, reduced = cse([e])
    assert substs == [(x0, x + y)]
    assert reduced == [sqrt(x0) + x0**2]

    subst42, (red42,) = cse([42])  # issue_15082
    assert len(subst42) == 0 and red42 == 42
    subst_half, (red_half,) = cse([0.5])
    assert len(subst_half) == 0 and red_half == 0.5

