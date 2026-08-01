
def test_uncouple_4_coupled_states_numerical():
    # j1=1/2, j2=1/2, j3=1, j4=1, default coupling
    assert uncouple(JzKetCoupled(3, 3, (S.Half, S.Half, 1, 1))) == \
        TensorProduct(JzKet(
            S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 1))
    assert uncouple(JzKetCoupled(3, 2, (S.Half, S.Half, 1, 1))) == \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 1))/6 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/6 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/3 + \
        sqrt(3)*TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/3
    assert uncouple(JzKetCoupled(3, 1, (S.Half, S.Half, 1, 1))) == \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/15 + \
        2*sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, 1), JzKet(1, -1))/15
    assert uncouple(JzKetCoupled(3, 0, (S.Half, S.Half, 1, 1))) == \
        sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/10 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/10 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/10 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/5 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/10 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/10 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/5 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/10 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/10 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, 0), JzKet(1, -1))/10
    assert uncouple(JzKetCoupled(3, -1, (S.Half, S.Half, 1, 1))) == \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/15 + \
        2*sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, -1), JzKet(1, -1))/15
    assert uncouple(JzKetCoupled(3, -2, (S.Half, S.Half, 1, 1))) == \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/3 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/3 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, -1))/6 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             Rational(-1, 2)), JzKet(1, -1), JzKet(1, -1))/6
    assert uncouple(JzKetCoupled(3, -3, (S.Half, S.Half, 1, 1))) == \
        TensorProduct(JzKet(S.Half, -S(
            1)/2), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, -1))
    assert uncouple(JzKetCoupled(2, 2, (S.Half, S.Half, 1, 1))) == \
        -sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 1))/6 - \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/6 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/6 + \
        sqrt(6)*TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/3
    assert uncouple(JzKetCoupled(2, 1, (S.Half, S.Half, 1, 1))) == \
        -sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/6 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/6 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/12 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/6 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/12 - \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/6 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/6 + \
        sqrt(3)*TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/3
    assert uncouple(JzKetCoupled(2, 0, (S.Half, S.Half, 1, 1))) == \
        -TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/2 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/4 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/4 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/4 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/4 + \
        TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(2, -1, (S.Half, S.Half, 1, 1))) == \
        -sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/3 - \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/6 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/6 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/12 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/6 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/12 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/6 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, -1), JzKet(1, -1))/6
    assert uncouple(JzKetCoupled(2, -2, (S.Half, S.Half, 1, 1))) == \
        -sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/3 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/6 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, -1))/6 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             Rational(-1, 2)), JzKet(1, -1), JzKet(1, -1))/6
    assert uncouple(JzKetCoupled(1, 1, (S.Half, S.Half, 1, 1))) == \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/30 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/30 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/20 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/30 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/20 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/30 - \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/10 + \
        sqrt(15)*TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/5
    assert uncouple(JzKetCoupled(1, 0, (S.Half, S.Half, 1, 1))) == \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/10 - \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/20 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/20 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/20 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/20 - \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, 0), JzKet(1, -1))/10
    assert uncouple(JzKetCoupled(1, -1, (S.Half, S.Half, 1, 1))) == \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/5 - \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/10 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/30 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/20 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/30 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/20 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/30 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, -1), JzKet(1, -1))/30
    # j1=1/2, j2=1/2, j3=1, j4=1, j12=1, j34=1
    assert uncouple(JzKetCoupled(2, 2, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 1), (1, 3, 2)))) == \
        -sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/2 + \
        sqrt(2)*TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/2
    assert uncouple(JzKetCoupled(2, 1, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 1), (1, 3, 2)))) == \
        -sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/4 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/4 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/4 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/4 - \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/2 + \
        TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(2, 0, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 1), (1, 3, 2)))) == \
        -sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/6 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/6 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/6 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/6 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/6 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/6 - \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/6 + \
        sqrt(3)*TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/6
    assert uncouple(JzKetCoupled(2, -1, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 1), (1, 3, 2)))) == \
        -TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/2 + \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/2 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/4 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/4 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/4 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/4
    assert uncouple(JzKetCoupled(2, -2, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 1), (1, 3, 2)))) == \
        -sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/2 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half,
             Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(1, 1, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 1), (1, 3, 1)))) == \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/4 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/4 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/4 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/4 - \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/2 + \
        TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(1, 0, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 1), (1, 3, 1)))) == \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/2 - \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/2 - \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/2 + \
        TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(1, -1, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 1), (1, 3, 1)))) == \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/2 - \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/2 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/4 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/4 - \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/4 + \
        sqrt(2)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/4
    # j1=1/2, j2=1/2, j3=1, j4=1, j12=1, j34=2
    assert uncouple(JzKetCoupled(3, 3, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 3)))) == \
        TensorProduct(JzKet(
            S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 1))
    assert uncouple(JzKetCoupled(3, 2, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 3)))) == \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 1))/6 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/6 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/3 + \
        sqrt(3)*TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/3
    assert uncouple(JzKetCoupled(3, 1, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 3)))) == \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/15 + \
        2*sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, 1), JzKet(1, -1))/15
    assert uncouple(JzKetCoupled(3, 0, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 3)))) == \
        sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/10 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/10 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/10 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/5 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/10 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/10 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/5 + \
        sqrt(5)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/10 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/10 + \
        sqrt(10)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, 0), JzKet(1, -1))/10
    assert uncouple(JzKetCoupled(3, -1, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 3)))) == \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/15 + \
        2*sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/15 + \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, -1), JzKet(1, -1))/15
    assert uncouple(JzKetCoupled(3, -2, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 3)))) == \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/3 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/3 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, -1))/6 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             Rational(-1, 2)), JzKet(1, -1), JzKet(1, -1))/6
    assert uncouple(JzKetCoupled(3, -3, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 3)))) == \
        TensorProduct(JzKet(S.Half, -S(
            1)/2), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, -1))
    assert uncouple(JzKetCoupled(2, 2, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 2)))) == \
        -sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 1))/3 - \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/3 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/6 + \
        sqrt(6)*TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/6
    assert uncouple(JzKetCoupled(2, 1, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 2)))) == \
        -sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/3 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/12 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/12 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/12 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/12 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/6 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/3 + \
        sqrt(3)*TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/6
    assert uncouple(JzKetCoupled(2, 0, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 2)))) == \
        -TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/2 - \
        TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/2 + \
        TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/2 + \
        TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/2
    assert uncouple(JzKetCoupled(2, -1, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 2)))) == \
        -sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/6 - \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/3 - \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/6 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/12 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/12 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/12 + \
        sqrt(6)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/12 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, -1), JzKet(1, -1))/3
    assert uncouple(JzKetCoupled(2, -2, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 2)))) == \
        -sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/6 - \
        sqrt(6)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/6 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, -1))/3 + \
        sqrt(3)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             Rational(-1, 2)), JzKet(1, -1), JzKet(1, -1))/3
    assert uncouple(JzKetCoupled(1, 1, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 1)))) == \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 1))/5 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 1))/20 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, 0))/20 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/20 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/20 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/30 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, 1), JzKet(1, -1))/30
    assert uncouple(JzKetCoupled(1, 0, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 1)))) == \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 1))/10 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, 0))/10 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 1))/30 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, 0))/15 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(1, -1))/30 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/30 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/15 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/30 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/10 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, 0), JzKet(1, -1))/10
    assert uncouple(JzKetCoupled(1, -1, (S.Half, S.Half, 1, 1), ((1, 2, 1), (3, 4, 2), (1, 3, 1)))) == \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 1))/30 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, 0))/15 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(1, -1))/30 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(1, 0))/20 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(1, -1))/20 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(1, 0))/20 - \
        sqrt(30)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(1, -1))/20 + \
        sqrt(15)*TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half,
             S.Half), JzKet(1, -1), JzKet(1, -1))/5

