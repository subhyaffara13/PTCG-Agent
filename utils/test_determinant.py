
def test_determinant(method, M, sol):
    assert M.det(method=method) == sol


def test_determinant():
    assert det(2*C) == 2**n*det(C)
    assert det(2*C*D) == 2**n*det(C)*det(D)
    assert det(3*C*A*A.T*D) == 3**n*det(C)*det(A*A.T)*det(D)

