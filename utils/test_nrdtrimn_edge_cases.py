
def test_nrdtrimn_edge_cases(p, std, x, ref):
    assert_equal(sp.nrdtrimn(p, std, x), ref)

