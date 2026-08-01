
def test_slice_issue_3401():
    assert zeros(0, 3)[:, -1].shape == (0, 1)
    assert zeros(3, 0)[0, :] == Matrix(1, 0, [])


def test_slice_issue_3401():
    assert zeros(0, 3)[:, -1].shape == (0, 1)
    assert zeros(3, 0)[0, :] == Matrix(1, 0, [])

