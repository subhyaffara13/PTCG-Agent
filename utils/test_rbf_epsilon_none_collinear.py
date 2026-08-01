
def test_rbf_epsilon_none_collinear():
    # Check that collinear points in one dimension doesn't cause an error
    # due to epsilon = 0
    x = [1, 2, 3]
    y = [4, 4, 4]
    z = [5, 6, 7]
    rbf = Rbf(x, y, z, epsilon=None)
    assert rbf.epsilon > 0

