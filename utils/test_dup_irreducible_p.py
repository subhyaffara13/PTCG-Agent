
def test_dup_irreducible_p():
    R, x = ring("x", ZZ)
    assert R.dup_irreducible_p(x**2 + x + 1) is True
    assert R.dup_irreducible_p(x**2 + 2*x + 1) is False

