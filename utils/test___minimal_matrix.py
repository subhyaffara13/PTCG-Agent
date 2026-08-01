
def test__MinimalMatrix():
    x = _MinimalMatrix(2, 3, [1, 2, 3, 4, 5, 6])
    assert x.rows == 2
    assert x.cols == 3
    assert x[2] == 3
    assert x[1, 1] == 5
    assert list(x) == [1, 2, 3, 4, 5, 6]
    assert list(x[1, :]) == [4, 5, 6]
    assert list(x[:, 1]) == [2, 5]
    assert list(x[:, :]) == list(x)
    assert x[:, :] == x
    assert _MinimalMatrix(x) == x
    assert _MinimalMatrix([[1, 2, 3], [4, 5, 6]]) == x
    assert _MinimalMatrix(([1, 2, 3], [4, 5, 6])) == x
    assert _MinimalMatrix([(1, 2, 3), (4, 5, 6)]) == x
    assert _MinimalMatrix(((1, 2, 3), (4, 5, 6))) == x
    assert not (_MinimalMatrix([[1, 2], [3, 4], [5, 6]]) == x)


def test__MinimalMatrix():
    x = Matrix(2, 3, [1, 2, 3, 4, 5, 6])
    assert x.rows == 2
    assert x.cols == 3
    assert x[2] == 3
    assert x[1, 1] == 5
    assert list(x) == [1, 2, 3, 4, 5, 6]
    assert list(x[1, :]) == [4, 5, 6]
    assert list(x[:, 1]) == [2, 5]
    assert list(x[:, :]) == list(x)
    assert x[:, :] == x
    assert Matrix(x) == x
    assert Matrix([[1, 2, 3], [4, 5, 6]]) == x
    assert Matrix(([1, 2, 3], [4, 5, 6])) == x
    assert Matrix([(1, 2, 3), (4, 5, 6)]) == x
    assert Matrix(((1, 2, 3), (4, 5, 6))) == x
    assert not (Matrix([[1, 2], [3, 4], [5, 6]]) == x)

