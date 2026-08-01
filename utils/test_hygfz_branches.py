
def test_hygfz_branches():
    """(z == 1.0) && (c-a-b > 0.0)"""
    res = special.hyp2f1(1.5, 2.5, 4.5, 1.+0.j)
    assert_allclose(res, 10.30835089459151+0j)
    """(cabs(z+1) < eps) && (fabs(c-a+b - 1.0) < eps)"""
    res = special.hyp2f1(5+5e-16, 2, 2, -1.0 + 5e-16j)
    assert_allclose(res, 0.031249999999999986+3.9062499999999994e-17j)

