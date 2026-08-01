
def test_dm_adj_det(name, A, A_inv, den):
    assert A.adj_det() == (A_inv, den)

