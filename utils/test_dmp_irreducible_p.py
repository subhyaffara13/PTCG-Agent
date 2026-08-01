
def test_dmp_irreducible_p():
    R, x, y = ring("x,y", ZZ)
    assert R.dmp_irreducible_p(x**2 + x + 1) is True
    assert R.dmp_irreducible_p(x**2 + 2*x + 1) is False

