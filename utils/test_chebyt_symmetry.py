
def test_chebyt_symmetry():
    x, w = sc.roots_chebyt(21)
    pos, neg = x[:10], x[11:]
    assert_equal(neg, -pos[::-1])
    assert_equal(x[10], 0)

