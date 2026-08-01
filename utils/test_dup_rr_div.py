
def test_dup_rr_div():
    raises(ZeroDivisionError, lambda: dup_rr_div([1, 2, 3], [], ZZ))

    f = dup_normal([3, 1, 1, 5], ZZ)
    g = dup_normal([5, -3, 1], ZZ)

    q, r = [], f

    assert dup_rr_div(f, g, ZZ) == (q, r)

