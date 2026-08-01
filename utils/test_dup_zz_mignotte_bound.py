
def test_dup_zz_mignotte_bound():
    R, x = ring("x", ZZ)
    assert R.dup_zz_mignotte_bound(2*x**2 + 3*x + 4) == 6
    assert R.dup_zz_mignotte_bound(x**3 + 14*x**2 + 56*x + 64) == 152

