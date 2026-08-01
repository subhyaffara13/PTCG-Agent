
def test_XXM_extract_slice(DM):
    A = DM([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert A.extract_slice(*_slice[:,:]) == A
    assert A.extract_slice(*_slice[1:,:]) == DM([[4, 5, 6], [7, 8, 9]])
    assert A.extract_slice(*_slice[1:,1:]) == DM([[5, 6], [8, 9]])
    assert A.extract_slice(*_slice[1:,:-1]) == DM([[4, 5], [7, 8]])
    assert A.extract_slice(*_slice[1:,:-1:2]) == DM([[4], [7]])
    assert A.extract_slice(*_slice[:,::2]) == DM([[1, 3], [4, 6], [7, 9]])
    assert A.extract_slice(*_slice[::2,:]) == DM([[1, 2, 3], [7, 8, 9]])
    assert A.extract_slice(*_slice[::2,::2]) == DM([[1, 3], [7, 9]])
    assert A.extract_slice(*_slice[::2,::-2]) == DM([[3, 1], [9, 7]])
    assert A.extract_slice(*_slice[::-2,::2]) == DM([[7, 9], [1, 3]])
    assert A.extract_slice(*_slice[::-2,::-2]) == DM([[9, 7], [3, 1]])
    assert A.extract_slice(*_slice[:,::-1]) == DM([[3, 2, 1], [6, 5, 4], [9, 8, 7]])
    assert A.extract_slice(*_slice[::-1,:]) == DM([[7, 8, 9], [4, 5, 6], [1, 2, 3]])

