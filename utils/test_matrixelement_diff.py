
def test_matrixelement_diff():
    dexpr = diff((D*w)[k,0], w[p,0])

    assert w[k, p].diff(w[k, p]) == 1
    assert w[k, p].diff(w[0, 0]) == KroneckerDelta(0, k, (0, n-1))*KroneckerDelta(0, p, (0, 0))
    _i_1 = Dummy("_i_1")
    assert dexpr.dummy_eq(Sum(KroneckerDelta(_i_1, p, (0, n-1))*D[k, _i_1], (_i_1, 0, n - 1)))
    assert dexpr.doit() == D[k, p]

