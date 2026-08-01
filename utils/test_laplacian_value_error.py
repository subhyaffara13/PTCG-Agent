
def test_laplacian_value_error():
    for t in int, float, complex:
        for m in ([1, 1],
                  [[[1]]],
                  [[1, 2, 3], [4, 5, 6]],
                  [[1, 2], [3, 4], [5, 5]]):
            A = np.array(m, dtype=t)
            assert_raises(ValueError, csgraph.laplacian, A)

