
def test_to_midstep_empty():
    steps = cbook.pts_to_midstep([], [])
    assert steps.shape == (2, 0)

