
def test_XDM_getitem(DM):
    """Test getitem for DDM, etc."""

    lol = [[0, 1], [2, 0]]
    A = DM(lol)
    m, n = A.shape

    indices = [-3, -2, -1, 0, 1, 2]

    for i in indices:
        for j in indices:
            if -2 <= i < m and -2 <= j < n:
                assert A.getitem(i, j) == ZZ(lol[i][j])
            else:
                raises(IndexError, lambda: A.getitem(i, j))

