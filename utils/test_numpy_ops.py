
def test_numpy_ops(numpy_op, expected):
    # GH8383
    result = numpy_op(Series([1, 2, 3, 4]))
    assert result == expected

