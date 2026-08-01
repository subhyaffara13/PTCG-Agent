
def test_M2():
    # The roots of this equation should all be real. Note that this
    # doesn't test that they are correct.
    sol = solveset(3*x**3 - 18*x**2 + 33*x - 19, x)
    assert all(s.expand(complex=True).is_real for s in sol)

