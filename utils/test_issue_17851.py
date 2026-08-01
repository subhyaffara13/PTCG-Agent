
def test_issue_17851():
    for array_type in array_types:
        A = array_type([])
        assert isinstance(A, array_type)
        assert A.shape == (0,)
        assert list(A) == []

