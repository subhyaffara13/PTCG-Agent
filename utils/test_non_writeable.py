
def test_non_writeable():
    mat = np.eye(4)
    mat.flags.writeable = False
    RigidTransform.from_matrix(mat)  # Regression test against gh-24378


def test_non_writeable():
    q = np.array([0, 0, 0, 1.0])
    q.flags.writeable = False
    Rotation.from_quat(q)  # Regression test against gh-24354, should not raise

