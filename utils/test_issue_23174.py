
def test_issue_23174():
    f = ZZ.map([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    g = ZZ.map([[1, 0, 0, 1, 1, 1, 0, 0, 1], [1, 1, 1, 0, 1, 0, 1, 1, 1]])

    assert gf_edf_zassenhaus(f, 8, 2, ZZ) == g

