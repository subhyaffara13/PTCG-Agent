
def test_inherited_protocol():
    """SquareMatrix is derived from Matrix and inherits the buffer protocol"""

    matrix = m.SquareMatrix(5)
    assert memoryview(matrix).shape == (5, 5)
    assert np.asarray(matrix).shape == (5, 5)

