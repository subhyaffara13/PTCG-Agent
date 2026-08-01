
def test_issue_25793():
    R, x = ring("x", ZZ)
    f = x - 4851  # failure starts for values more than 4850
    g = f*(2*x + 1)
    H, cff, cfg = R.dup_zz_heu_gcd(f, g)
    assert H == f

