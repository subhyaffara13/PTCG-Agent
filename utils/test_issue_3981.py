
def test_issue_3981():
    class Index1:
        def __index__(self):
            return 1

    class Index2:
        def __index__(self):
            return 2
    index1 = Index1()
    index2 = Index2()

    m = Matrix([1, 2, 3])

    assert m[index2] == 3

    m[index2] = 5
    assert m[2] == 5

    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m[index1, index2] == 6
    assert m[1, index2] == 6
    assert m[index1, 2] == 6

    m[index1, index2] = 4
    assert m[1, 2] == 4
    m[1, index2] = 6
    assert m[1, 2] == 6
    m[index1, 2] = 8
    assert m[1, 2] == 8


def test_issue_3981():
    class Index1:
        def __index__(self):
            return 1

    class Index2:
        def __index__(self):
            return 2
    index1 = Index1()
    index2 = Index2()

    m = Matrix([1, 2, 3])

    assert m[index2] == 3

    m[index2] = 5
    assert m[2] == 5

    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m[index1, index2] == 6
    assert m[1, index2] == 6
    assert m[index1, 2] == 6

    m[index1, index2] = 4
    assert m[1, 2] == 4
    m[1, index2] = 6
    assert m[1, 2] == 6
    m[index1, 2] = 8
    assert m[1, 2] == 8

