
def test_dup_zz_irreducible_p():
    R, x = ring("x", ZZ)

    assert R.dup_zz_irreducible_p(3*x**4 + 2*x**3 + 6*x**2 + 8*x + 7) is None
    assert R.dup_zz_irreducible_p(3*x**4 + 2*x**3 + 6*x**2 + 8*x + 4) is None

    assert R.dup_zz_irreducible_p(3*x**4 + 2*x**3 + 6*x**2 + 8*x + 10) is True
    assert R.dup_zz_irreducible_p(3*x**4 + 2*x**3 + 6*x**2 + 8*x + 14) is True

