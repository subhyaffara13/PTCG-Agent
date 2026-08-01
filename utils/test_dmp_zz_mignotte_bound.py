
def test_dmp_zz_mignotte_bound():
    R, x, y = ring("x,y", ZZ)
    assert R.dmp_zz_mignotte_bound(2*x**2 + 3*x + 4) == 32

