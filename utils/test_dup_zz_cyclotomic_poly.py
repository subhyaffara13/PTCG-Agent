
def test_dup_zz_cyclotomic_poly():
    R, x = ring("x", ZZ)

    assert R.dup_zz_cyclotomic_poly(1) == x - 1
    assert R.dup_zz_cyclotomic_poly(2) == x + 1
    assert R.dup_zz_cyclotomic_poly(3) == x**2 + x + 1
    assert R.dup_zz_cyclotomic_poly(4) == x**2 + 1
    assert R.dup_zz_cyclotomic_poly(5) == x**4 + x**3 + x**2 + x + 1
    assert R.dup_zz_cyclotomic_poly(6) == x**2 - x + 1
    assert R.dup_zz_cyclotomic_poly(7) == x**6 + x**5 + x**4 + x**3 + x**2 + x + 1
    assert R.dup_zz_cyclotomic_poly(8) == x**4 + 1
    assert R.dup_zz_cyclotomic_poly(9) == x**6 + x**3 + 1

