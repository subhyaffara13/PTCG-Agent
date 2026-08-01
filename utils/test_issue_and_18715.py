
def test_issue_and_18715():
    for array_type in mutable_array_types:
        A = array_type([0, 1, 2])
        A[0] += 5
        assert A[0] == 5

