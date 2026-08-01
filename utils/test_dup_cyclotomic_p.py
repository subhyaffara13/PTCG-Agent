
def test_dup_cyclotomic_p():
    R, x = ring("x", ZZ)

    assert R.dup_cyclotomic_p(x - 1) is True
    assert R.dup_cyclotomic_p(x + 1) is True
    assert R.dup_cyclotomic_p(x**2 + x + 1) is True
    assert R.dup_cyclotomic_p(x**2 + 1) is True
    assert R.dup_cyclotomic_p(x**4 + x**3 + x**2 + x + 1) is True
    assert R.dup_cyclotomic_p(x**2 - x + 1) is True
    assert R.dup_cyclotomic_p(x**6 + x**5 + x**4 + x**3 + x**2 + x + 1) is True
    assert R.dup_cyclotomic_p(x**4 + 1) is True
    assert R.dup_cyclotomic_p(x**6 + x**3 + 1) is True

    assert R.dup_cyclotomic_p(0) is False
    assert R.dup_cyclotomic_p(1) is False
    assert R.dup_cyclotomic_p(x) is False
    assert R.dup_cyclotomic_p(x + 2) is False
    assert R.dup_cyclotomic_p(3*x + 1) is False
    assert R.dup_cyclotomic_p(x**2 - 1) is False

    f = x**16 + x**14 - x**10 + x**8 - x**6 + x**2 + 1
    assert R.dup_cyclotomic_p(f) is False

    g = x**16 + x**14 - x**10 - x**8 - x**6 + x**2 + 1
    assert R.dup_cyclotomic_p(g) is True

    R, x = ring("x", QQ)
    assert R.dup_cyclotomic_p(x**2 + x + 1) is True
    assert R.dup_cyclotomic_p(QQ(1,2)*x**2 + x + 1) is False

    R, x = ring("x", ZZ["y"])
    assert R.dup_cyclotomic_p(x**2 + x + 1) is False

