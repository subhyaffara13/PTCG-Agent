
def test_PrimeIdeal_reduce():
    k = QQ.alg_field_from_poly(Poly(x ** 3 + x ** 2 - 2 * x + 8))
    Zk = k.maximal_order()
    P = k.primes_above(2)
    frp = P[2]

    # reduce_element
    a = Zk.parent(to_col([23, 20, 11]), denom=6)
    a_bar_expected = Zk.parent(to_col([11, 5, 2]), denom=6)
    a_bar = frp.reduce_element(a)
    assert a_bar == a_bar_expected

    # reduce_ANP
    a = k([QQ(11, 6), QQ(20, 6), QQ(23, 6)])
    a_bar_expected = k([QQ(2, 6), QQ(5, 6), QQ(11, 6)])
    a_bar = frp.reduce_ANP(a)
    assert a_bar == a_bar_expected

    # reduce_alg_num
    a = k.to_alg_num(a)
    a_bar_expected = k.to_alg_num(a_bar_expected)
    a_bar = frp.reduce_alg_num(a)
    assert a_bar == a_bar_expected

