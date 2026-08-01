
def test_uncouple_2_coupled_states_numerical():
    # j1=1/2, j2=1/2
    assert uncouple(JzKetCoupled(0, 0, (S.Half, S.Half))) == \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)))/2 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half))/2
    assert uncouple(JzKetCoupled(1, 1, (S.Half, S.Half))) == \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half))
    assert uncouple(JzKetCoupled(1, 0, (S.Half, S.Half))) == \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)))/2 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half))/2
    assert uncouple(JzKetCoupled(1, -1, (S.Half, S.Half))) == \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)))
    # j1=1, j2=1/2
    assert uncouple(JzKetCoupled(S.Half, S.Half, (1, S.Half))) == \
        -sqrt(3)*TensorProduct(JzKet(1, 0), JzKet(S.Half, S.Half))/3 + \
        sqrt(6)*TensorProduct(JzKet(1, 1), JzKet(S.Half, Rational(-1, 2)))/3
    assert uncouple(JzKetCoupled(S.Half, Rational(-1, 2), (1, S.Half))) == \
        sqrt(3)*TensorProduct(JzKet(1, 0), JzKet(S.Half, Rational(-1, 2)))/3 - \
        sqrt(6)*TensorProduct(JzKet(1, -1), JzKet(S.Half, S.Half))/3
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(3, 2), (1, S.Half))) == \
        TensorProduct(JzKet(1, 1), JzKet(S.Half, S.Half))
    assert uncouple(JzKetCoupled(Rational(3, 2), S.Half, (1, S.Half))) == \
        sqrt(3)*TensorProduct(JzKet(1, 1), JzKet(S.Half, Rational(-1, 2)))/3 + \
        sqrt(6)*TensorProduct(JzKet(1, 0), JzKet(S.Half, S.Half))/3
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(-1, 2), (1, S.Half))) == \
        sqrt(6)*TensorProduct(JzKet(1, 0), JzKet(S.Half, Rational(-1, 2)))/3 + \
        sqrt(3)*TensorProduct(JzKet(1, -1), JzKet(S.Half, S.Half))/3
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(-3, 2), (1, S.Half))) == \
        TensorProduct(JzKet(1, -1), JzKet(S.Half, Rational(-1, 2)))
    # j1=1, j2=1
    assert uncouple(JzKetCoupled(0, 0, (1, 1))) == \
        sqrt(3)*TensorProduct(JzKet(1, 1), JzKet(1, -1))/3 - \
        sqrt(3)*TensorProduct(JzKet(1, 0), JzKet(1, 0))/3 + \
        sqrt(3)*TensorProduct(JzKet(1, -1), JzKet(1, 1))/3
    assert uncouple(JzKetCoupled(1, 1, (1, 1))) == \
        sqrt(2)*TensorProduct(JzKet(1, 1), JzKet(1, 0))/2 - \
        sqrt(2)*TensorProduct(JzKet(1, 0), JzKet(1, 1))/2
    assert uncouple(JzKetCoupled(1, 0, (1, 1))) == \
        sqrt(2)*TensorProduct(JzKet(1, 1), JzKet(1, -1))/2 - \
        sqrt(2)*TensorProduct(JzKet(1, -1), JzKet(1, 1))/2
    assert uncouple(JzKetCoupled(1, -1, (1, 1))) == \
        sqrt(2)*TensorProduct(JzKet(1, 0), JzKet(1, -1))/2 - \
        sqrt(2)*TensorProduct(JzKet(1, -1), JzKet(1, 0))/2
    assert uncouple(JzKetCoupled(2, 2, (1, 1))) == \
        TensorProduct(JzKet(1, 1), JzKet(1, 1))
    assert uncouple(JzKetCoupled(2, 1, (1, 1))) == \
        sqrt(2)*TensorProduct(JzKet(1, 1), JzKet(1, 0))/2 + \
        sqrt(2)*TensorProduct(JzKet(1, 0), JzKet(1, 1))/2
    assert uncouple(JzKetCoupled(2, 0, (1, 1))) == \
        sqrt(6)*TensorProduct(JzKet(1, 1), JzKet(1, -1))/6 + \
        sqrt(6)*TensorProduct(JzKet(1, 0), JzKet(1, 0))/3 + \
        sqrt(6)*TensorProduct(JzKet(1, -1), JzKet(1, 1))/6
    assert uncouple(JzKetCoupled(2, -1, (1, 1))) == \
        sqrt(2)*TensorProduct(JzKet(1, 0), JzKet(1, -1))/2 + \
        sqrt(2)*TensorProduct(JzKet(1, -1), JzKet(1, 0))/2
    assert uncouple(JzKetCoupled(2, -2, (1, 1))) == \
        TensorProduct(JzKet(1, -1), JzKet(1, -1))

