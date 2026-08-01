
def test_hessenberg():
    A = Matrix([[3, 4, 1], [2, 4, 5], [0, 1, 2]])
    assert A.is_upper_hessenberg
    A = A.T
    assert A.is_lower_hessenberg
    A[0, -1] = 1
    assert A.is_lower_hessenberg is False

    A = Matrix([[3, 4, 1], [2, 4, 5], [3, 1, 2]])
    assert not A.is_upper_hessenberg

    A = zeros(5, 2)
    assert A.is_upper_hessenberg


def test_hessenberg():
    A = Matrix([[3, 4, 1], [2, 4, 5], [0, 1, 2]])
    assert A.is_upper_hessenberg
    A = A.T
    assert A.is_lower_hessenberg
    A[0, -1] = 1
    assert A.is_lower_hessenberg is False

    A = Matrix([[3, 4, 1], [2, 4, 5], [3, 1, 2]])
    assert not A.is_upper_hessenberg

    A = zeros(5, 2)
    assert A.is_upper_hessenberg

