
def test_to_prestep_empty():
    steps = cbook.pts_to_prestep([], [])
    assert steps.shape == (2, 0)

