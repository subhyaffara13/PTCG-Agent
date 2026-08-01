
def test_ConstantDenseOutput():
    sol = ConstantDenseOutput(0, 1, np.array([1, 2]))
    assert_allclose(sol(1.5), [1, 2])
    assert_allclose(sol([1, 1.5, 2]), [[1, 1, 1], [2, 2, 2]])

    sol = ConstantDenseOutput(0, 1, np.array([]))
    assert_allclose(sol(1.5), np.empty(0))
    assert_allclose(sol([1, 1.5, 2]), np.empty((0, 3)))

