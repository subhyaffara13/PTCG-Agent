
def test_cse_single2():
    # Simple substitution, test for being able to pass the expression directly
    e = Add(Pow(x + y, 2), sqrt(x + y))
    substs, reduced = cse(e)
    assert substs == [(x0, x + y)]
    assert reduced == [sqrt(x0) + x0**2]
    substs, reduced = cse(Matrix([[1]]))
    assert isinstance(reduced[0], Matrix)

    subst42, (red42,) = cse(42)  # issue 15082
    assert len(subst42) == 0 and red42 == 42
    subst_half, (red_half,) = cse(0.5)  # issue 15082
    assert len(subst_half) == 0 and red_half == 0.5

