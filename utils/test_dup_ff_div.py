
def test_dup_ff_div():
    raises(ZeroDivisionError, lambda: dup_ff_div([1, 2, 3], [], QQ))

    f = dup_normal([3, 1, 1, 5], QQ)
    g = dup_normal([5, -3, 1], QQ)

    q = [QQ(3, 5), QQ(14, 25)]
    r = [QQ(52, 25), QQ(111, 25)]

    assert dup_ff_div(f, g, QQ) == (q, r)

