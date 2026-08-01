
def test_XXM_lll(DM):
    M = DM([[1, 2, 3], [4, 5, 20]])
    M_lll = DM([[1, 2, 3], [-1, -5, 5]])
    T = DM([[1, 0], [-5, 1]])
    assert M.lll() == M_lll
    assert M.lll_transform() == (M_lll, T)
    assert T.matmul(M) == M_lll

