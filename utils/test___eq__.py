
def test___eq__():
    assert not QQ[x] == ZZ[x]
    assert not QQ.frac_field(x) == ZZ.frac_field(x)


def test___eq__():
    assert (Matrix(
        [[0, 1, 1],
        [1, 0, 0],
        [1, 1, 1]]) == {}) is False

