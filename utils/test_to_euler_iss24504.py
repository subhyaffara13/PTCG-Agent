
def test_to_euler_iss24504():
    """
    There was a mistake in the degenerate case testing
    See issue 24504 for reference.
    """
    q = Quaternion.from_euler((phi, 0, 0), 'zyz')
    assert trigsimp(q.to_euler('zyz'), inverse=True) == (phi, 0, 0)

