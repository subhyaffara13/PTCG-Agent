
def test_operator_dagger():
    A = Operator('A')
    B = Operator('B')
    assert Dagger(A*B) == Dagger(B)*Dagger(A)
    assert Dagger(A + B) == Dagger(A) + Dagger(B)
    assert Dagger(A**2) == Dagger(A)**2

