
def test_dagger_mul():
    O = Operator('O')
    assert Dagger(O)*O == Dagger(O)*O
    with warns_deprecated_sympy():
        I = IdentityOperator()
        assert Dagger(O)*O*I == Mul(Dagger(O), O)*I
    assert Dagger(O)*Dagger(O) == Dagger(O)**2
    assert Dagger(O)*Dagger(I) == Dagger(O)

