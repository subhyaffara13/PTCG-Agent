
def test_issue3044():
    expr1 = TensorProduct(Jz*JzKet(S(2),S.NegativeOne)/sqrt(2), Jz*JzKet(S.Half,S.Half))
    result = Mul(S.NegativeOne, Rational(1, 4), 2**S.Half, hbar**2)
    result *= TensorProduct(JzKet(2,-1), JzKet(S.Half,S.Half))
    assert qapply(expr1) == result

