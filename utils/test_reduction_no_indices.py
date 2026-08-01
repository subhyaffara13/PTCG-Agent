
def test_reduction_no_indices(xp):
    r = Rotation.from_quat(xp.asarray([0.0, 0.0, 0.0, 1.0]))
    result = r.reduce(return_indices=False)
    assert isinstance(result, Rotation)

