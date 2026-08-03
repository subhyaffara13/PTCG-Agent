import math


def test_repr_rotation_sequence(xp):
    q = xp.asarray([[0.0, 1, 0, 1], [0, 0, 1, 1]]) / math.sqrt(2)
    actual = f"{Rotation.from_quat(q)!r}"
    if is_numpy(xp):
        expected = """\
Rotation.from_matrix(array([[[ 0.,  0.,  1.],
                             [ 0.,  1.,  0.],
                             [-1.,  0.,  0.]],

                            [[ 0., -1.,  0.],
                             [ 1.,  0.,  0.],
                             [ 0.,  0.,  1.]]]))"""
        def stripped(s: str) -> str:
            # don't fail due to leading whitespace differences
            return "\n".join(map(str.lstrip, s.splitlines()))

        assert stripped(actual) == stripped(expected)
    else:
        assert actual.startswith("Rotation.from_matrix(")

