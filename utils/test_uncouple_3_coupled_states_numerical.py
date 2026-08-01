
def test_uncouple_3_coupled_states_numerical():
    # Default coupling
    # j1=1/2, j2=1/2, j3=1/2
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half))) == \
        TensorProduct(JzKet(
            S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half))
    assert uncouple(JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half))) == \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half))/3 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half))/3 + \
        sqrt(3)*TensorProduct(JzKet(
            S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)))/3
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half))) == \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half))/3 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)))/3 + \
        sqrt(3)*TensorProduct(JzKet(
            S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)))/3
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half))) == \
        TensorProduct(JzKet(
            S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)))
    # j1=1/2, j2=1/2, j3=1
    assert uncouple(JzKetCoupled(2, 2, (S.Half, S.Half, 1))) == \
        TensorProduct(
            JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1))
    assert uncouple(JzKetCoupled(2, 1, (S.Half, S.Half, 1))) == \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1))/2 + \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1))/2 + \
        sqrt(2)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0))/2
    assert uncouple(JzKetCoupled(2, 0, (S.Half, S.Half, 1))) == \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1))/6 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0))/3 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0))/3 + \
        sqrt(6)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1))/6
    assert uncouple(JzKetCoupled(2, -1, (S.Half, S.Half, 1))) == \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0))/2 + \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1))/2 + \
        TensorProduct(
            JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(2, -2, (S.Half, S.Half, 1))) == \
        TensorProduct(
            JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1))
    assert uncouple(JzKetCoupled(1, 1, (S.Half, S.Half, 1))) == \
        -TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1))/2 - \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1))/2 + \
        sqrt(2)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0))/2
    assert uncouple(JzKetCoupled(1, 0, (S.Half, S.Half, 1))) == \
        -sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1))/2 + \
        sqrt(2)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(1, -1, (S.Half, S.Half, 1))) == \
        -sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0))/2 + \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1))/2 + \
        TensorProduct(
            JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1))/2
    # j1=1/2, j2=1, j3=1
    assert uncouple(JzKetCoupled(Rational(5, 2), Rational(5, 2), (S.Half, 1, 1))) == \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 1))
    assert uncouple(JzKetCoupled(Rational(5, 2), Rational(3, 2), (S.Half, 1, 1))) == \
        sqrt(5)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/5 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/5 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1),
             JzKet(1, 0))/5
    assert uncouple(JzKetCoupled(Rational(5, 2), S.Half, (S.Half, 1, 1))) == \
        sqrt(5)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/5 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/5 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/10 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/5 + \
        sqrt(10)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/10
    assert uncouple(JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, 1, 1))) == \
        sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/10 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/5 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/10 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/5 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0),
             JzKet(1, -1))/5
    assert uncouple(JzKetCoupled(Rational(5, 2), Rational(-3, 2), (S.Half, 1, 1))) == \
        sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/5 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/5 + \
        sqrt(5)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, -1))/5
    assert uncouple(JzKetCoupled(Rational(5, 2), Rational(-5, 2), (S.Half, 1, 1))) == \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, -1))
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, 1, 1))) == \
        -sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/15 - \
        2*sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1),
             JzKet(1, 0))/5
    assert uncouple(JzKetCoupled(Rational(3, 2), S.Half, (S.Half, 1, 1))) == \
        -4*sqrt(5)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/15 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/15 - \
        2*sqrt(10)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/15 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1),
             JzKet(1, -1))/5
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, 1, 1))) == \
        -sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/5 - \
        sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/15 + \
        2*sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/15 - \
        sqrt(5)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/15 + \
        4*sqrt(5)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/15
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, 1, 1))) == \
        -sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/5 + \
        2*sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/15 + \
        sqrt(30)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, -1))/15
    assert uncouple(JzKetCoupled(S.Half, S.Half, (S.Half, 1, 1))) == \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/3 - \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/3 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/6 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/3 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1),
             JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, 1, 1))) == \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/2 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/3 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/6 - \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/3 + \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/3
    # j1=1, j2=1, j3=1
    assert uncouple(JzKetCoupled(3, 3, (1, 1, 1))) == \
        TensorProduct(JzKet(1, 1), JzKet(1, 1), JzKet(1, 1))
    assert uncouple(JzKetCoupled(3, 2, (1, 1, 1))) == \
        sqrt(3)*TensorProduct(JzKet(1, 0), JzKet(1, 1), JzKet(1, 1))/3 + \
        sqrt(3)*TensorProduct(JzKet(1, 1), JzKet(1, 0), JzKet(1, 1))/3 + \
        sqrt(3)*TensorProduct(JzKet(1, 1), JzKet(1, 1), JzKet(1, 0))/3
    assert uncouple(JzKetCoupled(3, 1, (1, 1, 1))) == \
        sqrt(15)*TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, 1))/15 + \
        2*sqrt(15)*TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, 1))/15 + \
        2*sqrt(15)*TensorProduct(JzKet(1, 0), JzKet(1, 1), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, 1))/15 + \
        2*sqrt(15)*TensorProduct(JzKet(1, 1), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(1, 1), JzKet(1, 1), JzKet(1, -1))/15
    assert uncouple(JzKetCoupled(3, 0, (1, 1, 1))) == \
        sqrt(10)*TensorProduct(JzKet(1, -1), JzKet(1, 0), JzKet(1, 1))/10 + \
        sqrt(10)*TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, 0))/10 + \
        sqrt(10)*TensorProduct(JzKet(1, 0), JzKet(1, -1), JzKet(1, 1))/10 + \
        sqrt(10)*TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, 0))/5 + \
        sqrt(10)*TensorProduct(JzKet(1, 0), JzKet(1, 1), JzKet(1, -1))/10 + \
        sqrt(10)*TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, 0))/10 + \
        sqrt(10)*TensorProduct(JzKet(1, 1), JzKet(1, 0), JzKet(1, -1))/10
    assert uncouple(JzKetCoupled(3, -1, (1, 1, 1))) == \
        sqrt(15)*TensorProduct(JzKet(1, -1), JzKet(1, -1), JzKet(1, 1))/15 + \
        2*sqrt(15)*TensorProduct(JzKet(1, -1), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, -1))/15 + \
        2*sqrt(15)*TensorProduct(JzKet(1, 0), JzKet(1, -1), JzKet(1, 0))/15 + \
        2*sqrt(15)*TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, -1))/15 + \
        sqrt(15)*TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, -1))/15
    assert uncouple(JzKetCoupled(3, -2, (1, 1, 1))) == \
        sqrt(3)*TensorProduct(JzKet(1, -1), JzKet(1, -1), JzKet(1, 0))/3 + \
        sqrt(3)*TensorProduct(JzKet(1, -1), JzKet(1, 0), JzKet(1, -1))/3 + \
        sqrt(3)*TensorProduct(JzKet(1, 0), JzKet(1, -1), JzKet(1, -1))/3
    assert uncouple(JzKetCoupled(3, -3, (1, 1, 1))) == \
        TensorProduct(JzKet(1, -1), JzKet(1, -1), JzKet(1, -1))
    assert uncouple(JzKetCoupled(2, 2, (1, 1, 1))) == \
        -sqrt(6)*TensorProduct(JzKet(1, 0), JzKet(1, 1), JzKet(1, 1))/6 - \
        sqrt(6)*TensorProduct(JzKet(1, 1), JzKet(1, 0), JzKet(1, 1))/6 + \
        sqrt(6)*TensorProduct(JzKet(1, 1), JzKet(1, 1), JzKet(1, 0))/3
    assert uncouple(JzKetCoupled(2, 1, (1, 1, 1))) == \
        -sqrt(3)*TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, 1))/6 - \
        sqrt(3)*TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, 1))/3 + \
        sqrt(3)*TensorProduct(JzKet(1, 0), JzKet(1, 1), JzKet(1, 0))/6 - \
        sqrt(3)*TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, 1))/6 + \
        sqrt(3)*TensorProduct(JzKet(1, 1), JzKet(1, 0), JzKet(1, 0))/6 + \
        sqrt(3)*TensorProduct(JzKet(1, 1), JzKet(1, 1), JzKet(1, -1))/3
    assert uncouple(JzKetCoupled(2, 0, (1, 1, 1))) == \
        -TensorProduct(JzKet(1, -1), JzKet(1, 0), JzKet(1, 1))/2 - \
        TensorProduct(JzKet(1, 0), JzKet(1, -1), JzKet(1, 1))/2 + \
        TensorProduct(JzKet(1, 0), JzKet(1, 1), JzKet(1, -1))/2 + \
        TensorProduct(JzKet(1, 1), JzKet(1, 0), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(2, -1, (1, 1, 1))) == \
        -sqrt(3)*TensorProduct(JzKet(1, -1), JzKet(1, -1), JzKet(1, 1))/3 - \
        sqrt(3)*TensorProduct(JzKet(1, -1), JzKet(1, 0), JzKet(1, 0))/6 + \
        sqrt(3)*TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, -1))/6 - \
        sqrt(3)*TensorProduct(JzKet(1, 0), JzKet(1, -1), JzKet(1, 0))/6 + \
        sqrt(3)*TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, -1))/3 + \
        sqrt(3)*TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, -1))/6
    assert uncouple(JzKetCoupled(2, -2, (1, 1, 1))) == \
        -sqrt(6)*TensorProduct(JzKet(1, -1), JzKet(1, -1), JzKet(1, 0))/3 + \
        sqrt(6)*TensorProduct(JzKet(1, -1), JzKet(1, 0), JzKet(1, -1))/6 + \
        sqrt(6)*TensorProduct(JzKet(1, 0), JzKet(1, -1), JzKet(1, -1))/6
    assert uncouple(JzKetCoupled(1, 1, (1, 1, 1))) == \
        sqrt(15)*TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, 1))/30 + \
        sqrt(15)*TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, 1))/15 - \
        sqrt(15)*TensorProduct(JzKet(1, 0), JzKet(1, 1), JzKet(1, 0))/10 + \
        sqrt(15)*TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, 1))/30 - \
        sqrt(15)*TensorProduct(JzKet(1, 1), JzKet(1, 0), JzKet(1, 0))/10 + \
        sqrt(15)*TensorProduct(JzKet(1, 1), JzKet(1, 1), JzKet(1, -1))/5
    assert uncouple(JzKetCoupled(1, 0, (1, 1, 1))) == \
        sqrt(15)*TensorProduct(JzKet(1, -1), JzKet(1, 0), JzKet(1, 1))/10 - \
        sqrt(15)*TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(1, 0), JzKet(1, -1), JzKet(1, 1))/10 - \
        2*sqrt(15)*TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(1, 0), JzKet(1, 1), JzKet(1, -1))/10 - \
        sqrt(15)*TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(1, 1), JzKet(1, 0), JzKet(1, -1))/10
    assert uncouple(JzKetCoupled(1, -1, (1, 1, 1))) == \
        sqrt(15)*TensorProduct(JzKet(1, -1), JzKet(1, -1), JzKet(1, 1))/5 - \
        sqrt(15)*TensorProduct(JzKet(1, -1), JzKet(1, 0), JzKet(1, 0))/10 + \
        sqrt(15)*TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, -1))/30 - \
        sqrt(15)*TensorProduct(JzKet(1, 0), JzKet(1, -1), JzKet(1, 0))/10 + \
        sqrt(15)*TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, -1))/15 + \
        sqrt(15)*TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, -1))/30
    # Defined j13
    # j1=1/2, j2=1/2, j3=1, j13=1/2
    assert uncouple(JzKetCoupled(1, 1, (S.Half, S.Half, 1), ((1, 3, S.Half), (1, 2, 1)) )) == \
        -sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1))/3 + \
        sqrt(3)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0))/3
    assert uncouple(JzKetCoupled(1, 0, (S.Half, S.Half, 1), ((1, 3, S.Half), (1, 2, 1)) )) == \
        -sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1))/3 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0))/6 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0))/6 + \
        sqrt(3)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1))/3
    assert uncouple(JzKetCoupled(1, -1, (S.Half, S.Half, 1), ((1, 3, S.Half), (1, 2, 1)) )) == \
        -sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0))/3 + \
        sqrt(6)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1))/3
    # j1=1/2, j2=1, j3=1, j13=1/2
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, 1, 1), ((1, 3, S.Half), (1, 2, Rational(3, 2))))) == \
        -sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/3 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1),
             JzKet(1, 0))/3
    assert uncouple(JzKetCoupled(Rational(3, 2), S.Half, (S.Half, 1, 1), ((1, 3, S.Half), (1, 2, Rational(3, 2))))) == \
        -2*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/3 - \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/3 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/3 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1),
             JzKet(1, -1))/3
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, 1, 1), ((1, 3, S.Half), (1, 2, Rational(3, 2))))) == \
        -sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/3 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/3 + \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/3 + \
        2*TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/3
    assert uncouple(JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, 1, 1), ((1, 3, S.Half), (1, 2, Rational(3, 2))))) == \
        -sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/3 + \
        sqrt(6)*TensorProduct(
            JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, -1))/3
    # j1=1, j2=1, j3=1, j13=1
    assert uncouple(JzKetCoupled(2, 2, (1, 1, 1), ((1, 3, 1), (1, 2, 2)))) == \
        -sqrt(2)*TensorProduct(JzKet(1, 0), JzKet(1, 1), JzKet(1, 1))/2 + \
        sqrt(2)*TensorProduct(JzKet(1, 1), JzKet(1, 1), JzKet(1, 0))/2
    assert uncouple(JzKetCoupled(2, 1, (1, 1, 1), ((1, 3, 1), (1, 2, 2)))) == \
        -TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, 1))/2 - \
        TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, 1))/2 + \
        TensorProduct(JzKet(1, 1), JzKet(1, 0), JzKet(1, 0))/2 + \
        TensorProduct(JzKet(1, 1), JzKet(1, 1), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(2, 0, (1, 1, 1), ((1, 3, 1), (1, 2, 2)))) == \
        -sqrt(3)*TensorProduct(JzKet(1, -1), JzKet(1, 0), JzKet(1, 1))/3 - \
        sqrt(3)*TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, 0))/6 - \
        sqrt(3)*TensorProduct(JzKet(1, 0), JzKet(1, -1), JzKet(1, 1))/6 + \
        sqrt(3)*TensorProduct(JzKet(1, 0), JzKet(1, 1), JzKet(1, -1))/6 + \
        sqrt(3)*TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, 0))/6 + \
        sqrt(3)*TensorProduct(JzKet(1, 1), JzKet(1, 0), JzKet(1, -1))/3
    assert uncouple(JzKetCoupled(2, -1, (1, 1, 1), ((1, 3, 1), (1, 2, 2)))) == \
        -TensorProduct(JzKet(1, -1), JzKet(1, -1), JzKet(1, 1))/2 - \
        TensorProduct(JzKet(1, -1), JzKet(1, 0), JzKet(1, 0))/2 + \
        TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, -1))/2 + \
        TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(2, -2, (1, 1, 1), ((1, 3, 1), (1, 2, 2)))) == \
        -sqrt(2)*TensorProduct(JzKet(1, -1), JzKet(1, -1), JzKet(1, 0))/2 + \
        sqrt(2)*TensorProduct(JzKet(1, 0), JzKet(1, -1), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(1, 1, (1, 1, 1), ((1, 3, 1), (1, 2, 1)))) == \
        TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, 1))/2 - \
        TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, 1))/2 + \
        TensorProduct(JzKet(1, 1), JzKet(1, 0), JzKet(1, 0))/2 - \
        TensorProduct(JzKet(1, 1), JzKet(1, 1), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(1, 0, (1, 1, 1), ((1, 3, 1), (1, 2, 1)))) == \
        TensorProduct(JzKet(1, -1), JzKet(1, 1), JzKet(1, 0))/2 - \
        TensorProduct(JzKet(1, 0), JzKet(1, -1), JzKet(1, 1))/2 - \
        TensorProduct(JzKet(1, 0), JzKet(1, 1), JzKet(1, -1))/2 + \
        TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, 0))/2
    assert uncouple(JzKetCoupled(1, -1, (1, 1, 1), ((1, 3, 1), (1, 2, 1)))) == \
        -TensorProduct(JzKet(1, -1), JzKet(1, -1), JzKet(1, 1))/2 + \
        TensorProduct(JzKet(1, -1), JzKet(1, 0), JzKet(1, 0))/2 - \
        TensorProduct(JzKet(1, 0), JzKet(1, 0), JzKet(1, -1))/2 + \
        TensorProduct(JzKet(1, 1), JzKet(1, -1), JzKet(1, -1))/2

