
def test_ProductSet__len__():
    A = FiniteSet(1, 2)
    B = FiniteSet(1, 2, 3)
    assert ProductSet(A).__len__() == 2
    assert ProductSet(A).__len__() is not S(2)
    assert ProductSet(A, B).__len__() == 6
    assert ProductSet(A, B).__len__() is not S(6)

