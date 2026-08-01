
def test_Matrix_array():
    class matarray:
        def __array__(self, dtype=object, copy=None):
            if copy is not None and not copy:
                raise TypeError("Cannot implement copy=False when converting Matrix to ndarray")
            from numpy import array
            return array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    matarr = matarray()
    assert Matrix(matarr) == Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

