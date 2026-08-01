
def test_issue_25282():
    dd = sd = [0] * 11 + [1]
    ds = [2, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0]
    ss = ds.copy()
    ss[8] = 2

    def rotate(x, i):
        return x[i:] + x[:i]

    mat = []
    for i in range(12):
        mat.append(rotate(ss, i) + rotate(sd, i))
    for i in range(12):
        mat.append(rotate(ds, i) + rotate(dd, i))

    assert sum(Matrix(mat).eigenvals().values()) == 24

