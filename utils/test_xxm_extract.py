
def test_XXM_extract(DM):

    A = DM([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    assert A.extract([0, 1, 2], [0, 1, 2]) == A
    assert A.extract([1, 2], [1, 2]) == DM([[5, 6], [8, 9]])
    assert A.extract([1, 2], [0, 1]) == DM([[4, 5], [7, 8]])
    assert A.extract([1, 2], [0, 2]) == DM([[4, 6], [7, 9]])
    assert A.extract([1, 2], [0]) == DM([[4], [7]])
    assert A.extract([1, 2], []) == DM([[1]]).zeros((2, 0), ZZ)
    assert A.extract([], [0, 1, 2]) == DM([[1]]).zeros((0, 3), ZZ)

    raises(IndexError, lambda: A.extract([1, 2], [0, 3]))
    raises(IndexError, lambda: A.extract([1, 2], [0, -4]))
    raises(IndexError, lambda: A.extract([3, 1], [0, 1]))
    raises(IndexError, lambda: A.extract([-4, 2], [3, 1]))

    B = DM([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    assert B.extract([1, 2], [1, 2]) == DM([[0, 0], [0, 0]])

