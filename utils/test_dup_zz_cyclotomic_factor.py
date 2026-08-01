
def test_dup_zz_cyclotomic_factor():
    R, x = ring("x", ZZ)

    assert R.dup_zz_cyclotomic_factor(0) is None
    assert R.dup_zz_cyclotomic_factor(1) is None

    assert R.dup_zz_cyclotomic_factor(2*x**10 - 1) is None
    assert R.dup_zz_cyclotomic_factor(x**10 - 3) is None
    assert R.dup_zz_cyclotomic_factor(x**10 + x**5 - 1) is None

    assert R.dup_zz_cyclotomic_factor(x + 1) == [x + 1]
    assert R.dup_zz_cyclotomic_factor(x - 1) == [x - 1]

    assert R.dup_zz_cyclotomic_factor(x**2 + 1) == [x**2 + 1]
    assert R.dup_zz_cyclotomic_factor(x**2 - 1) == [x - 1, x + 1]

    assert R.dup_zz_cyclotomic_factor(x**27 + 1) == \
        [x + 1, x**2 - x + 1, x**6 - x**3 + 1, x**18 - x**9 + 1]
    assert R.dup_zz_cyclotomic_factor(x**27 - 1) == \
        [x - 1, x**2 + x + 1, x**6 + x**3 + 1, x**18 + x**9 + 1]

