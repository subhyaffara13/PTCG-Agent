
def test_reduction_none_indices(xp):
    r = Rotation.from_quat(xp.asarray([0.0, 0.0, 0.0, 1.0]))
    result = r.reduce(return_indices=True)
    assert type(result) is tuple
    assert len(result) == 3

    reduced, left_best, right_best = result
    assert left_best is None
    assert right_best is None

