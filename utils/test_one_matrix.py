
def test_one_matrix():
    assert MatMul(x.T, OneMatrix(k, 1)).diff(x) == OneMatrix(k, 1)

