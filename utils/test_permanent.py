
def test_permanent():
    M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert M.per() == 450
    for i in range(1, 12):
        assert ones(i, i).per() == ones(i, i).T.per() == factorial(i)
        assert (ones(i, i)-eye(i)).per() == (ones(i, i)-eye(i)).T.per() == subfactorial(i)

    a1, a2, a3, a4, a5 = symbols('a_1 a_2 a_3 a_4 a_5')
    M = Matrix([a1, a2, a3, a4, a5])
    assert M.per() == M.T.per() == a1 + a2 + a3 + a4 + a5


def test_permanent():
    assert isinstance(Permanent(A), Permanent)
    assert not isinstance(Permanent(A), MatrixExpr)
    assert isinstance(Permanent(C), Permanent)
    assert Permanent(ones(3, 3)).doit() == 6
    _ = C / per(C)
    assert per(Matrix(3, 3, [1, 3, 2, 4, 1, 3, 2, 5, 2])) == 103
    raises(TypeError, lambda: Permanent(S.One))
    assert Permanent(A).arg is A

