
def test_is_nilpotent():
    a = Matrix(4, 4, [0, 2, 1, 6, 0, 0, 1, 2, 0, 0, 0, 3, 0, 0, 0, 0])
    assert a.is_nilpotent()
    a = Matrix([[1, 0], [0, 1]])
    assert not a.is_nilpotent()
    a = Matrix([])
    assert a.is_nilpotent()


def test_is_nilpotent():
    a = Matrix(4, 4, [0, 2, 1, 6, 0, 0, 1, 2, 0, 0, 0, 3, 0, 0, 0, 0])
    assert a.is_nilpotent()
    a = Matrix([[1, 0], [0, 1]])
    assert not a.is_nilpotent()
    a = Matrix([])
    assert a.is_nilpotent()


def test_is_nilpotent():
    # every abelian group is nilpotent
    for i in (1, 2, 3):
        C = CyclicGroup(i)
        Ab = AbelianGroup(i, i + 2)
        assert C.is_nilpotent
        assert Ab.is_nilpotent
    Ab = AbelianGroup(5, 7, 10)
    assert Ab.is_nilpotent
    # A_5 is not solvable and thus not nilpotent
    assert AlternatingGroup(5).is_nilpotent is False

