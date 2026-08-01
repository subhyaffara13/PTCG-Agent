
def test_regression_gh24141():
    c = np.ones(8, dtype=np.int64)
    integrality = c.copy()

    b = np.asarray([42, 252, 277, 41, 222, 48], dtype=np.int64)
    a = np.asarray([
        [0, 1, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 1],
        [0, 1, 1, 1, 0, 1, 1, 0],
    ], dtype=np.int64)

    res = milp(c, integrality=integrality, constraints=(a, b, b))

    assert res.success
    assert_allclose(a @ res.x, b)

