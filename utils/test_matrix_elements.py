
def test_matrix_elements():
    b = VarBosonicBasis(5)
    o = B(0)
    m = matrix_rep(o, b)
    for i in range(4):
        assert m[i, i + 1] == sqrt(i + 1)
    o = Bd(0)
    m = matrix_rep(o, b)
    for i in range(4):
        assert m[i + 1, i] == sqrt(i + 1)

