
def test_comparisons_forwards_error(op):
    class NotArray:
        def __array__(self, dtype=None, copy=None):
            raise TypeError("run you fools")

    with pytest.raises(TypeError, match="run you fools"):
        op(np.arange(2), NotArray())

    with pytest.raises(TypeError, match="run you fools"):
        op(NotArray(), np.arange(2))

