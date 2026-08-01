
def test_repr_single_rotation(xp):
    q = xp.asarray([0, 0, 0, 1])
    actual = repr(Rotation.from_quat(q))
    if is_numpy(xp):
        expected = """\
Rotation.from_matrix(array([[1., 0., 0.],
                            [0., 1., 0.],
                            [0., 0., 1.]]))"""
        assert actual == expected
    else:
        assert actual.startswith("Rotation.from_matrix(")

