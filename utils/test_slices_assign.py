
def test_slices_assign():
    a = MutableDenseNDimArray(range(12), shape=(4, 3))
    b = MutableSparseNDimArray(range(12), shape=(4, 3))

    for i in [a, b]:
        assert i.tolist() == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
        i[0, :] = [2, 2, 2]
        assert i.tolist() == [[2, 2, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
        i[0, 1:] = [8, 8]
        assert i.tolist() == [[2, 8, 8], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
        i[1:3, 1] = [20, 44]
        assert i.tolist() == [[2, 8, 8], [3, 20, 5], [6, 44, 8], [9, 10, 11]]

