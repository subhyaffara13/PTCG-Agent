
def test_to_poststep_empty():
    steps = cbook.pts_to_poststep([], [])
    assert steps.shape == (2, 0)

