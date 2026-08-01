
def test_joint_vector_expectation():
    m = Normal('A', [x, y], [[1, 0], [0, 1]])
    assert E(m) == (x, y)

