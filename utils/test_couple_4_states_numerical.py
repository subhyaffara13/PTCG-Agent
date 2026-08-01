
def test_couple_4_states_numerical():
    # Default coupling
    # j1=1/2, j2=1/2, j3=1/2, j4=1/2
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half))) == \
        JzKetCoupled(2, 2, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)))) == \
        sqrt(3)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/2 + \
        JzKetCoupled(2, 1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half))) == \
        sqrt(6)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)) )/3 - \
        sqrt(3)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/6 + \
        JzKetCoupled(2, 1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)))) == \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 0)) )/3 + \
        sqrt(3)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)) )/3 + \
        sqrt(6)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/6 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/6
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half))) == \
        sqrt(2)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (1, 3, S.Half), (1, 4, 1)) )/2 - \
        sqrt(6)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)) )/6 - \
        sqrt(3)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/6 + \
        JzKetCoupled(2, 1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)),
                        JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)))) == \
        JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half),
                ((1, 2, 0), (1, 3, S.Half), (1, 4, 0)))/2 - \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half),
                ((1, 2, 1), (1, 3, S.Half), (1, 4, 0)))/6 + \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half),
                ((1, 2, 0), (1, 3, S.Half), (1, 4, 1)))/2 - \
        sqrt(3)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half),
                ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)))/6 + \
        sqrt(6)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half),
                ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)))/6 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S.Half, S.Half, S.Half),
                ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)))/6
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half))) == \
        -JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (1, 3, S.Half), (1, 4, 0)) )/2 - \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 0)) )/6 + \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (1, 3, S.Half), (1, 4, 1)) )/2 + \
        sqrt(3)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)) )/6 - \
        sqrt(6)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/6 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/6
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)))) == \
        sqrt(2)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (1, 3, S.Half), (1, 4, 1)) )/2 + \
        sqrt(6)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)) )/6 + \
        sqrt(3)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/6 + \
        JzKetCoupled(2, -1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half))) == \
        -sqrt(2)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (1, 3, S.Half), (1, 4, 1)) )/2 - \
        sqrt(6)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)) )/6 - \
        sqrt(3)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/6 + \
        JzKetCoupled(2, 1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)))) == \
        -JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (1, 3, S.Half), (1, 4, 0)) )/2 - \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 0)) )/6 - \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (1, 3, S.Half), (1, 4, 1)) )/2 - \
        sqrt(3)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)) )/6 + \
        sqrt(6)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/6 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/6
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half))) == \
        JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (1, 3, S.Half), (1, 4, 0)) )/2 - \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 0)) )/6 - \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (1, 3, S.Half), (1, 4, 1)) )/2 + \
        sqrt(3)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)) )/6 - \
        sqrt(6)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/6 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/6
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)))) == \
        -sqrt(2)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (1, 3, S.Half), (1, 4, 1)) )/2 + \
        sqrt(6)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)) )/6 + \
        sqrt(3)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/6 + \
        JzKetCoupled(2, -1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half))) == \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 0)) )/3 - \
        sqrt(3)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)) )/3 - \
        sqrt(6)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/6 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/6
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)))) == \
        -sqrt(6)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, S.Half), (1, 4, 1)) )/3 + \
        sqrt(3)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/6 + \
        JzKetCoupled(2, -1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half))) == \
        -sqrt(3)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 1)) )/2 + \
        JzKetCoupled(2, -1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)))) == \
        JzKetCoupled(2, -2, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, 2)) )
    # j1=S.Half, S.Half, S.Half, 1
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1))) == \
        JzKetCoupled(Rational(5, 2), Rational(5, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0))) == \
        sqrt(15)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/5 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1))) == \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/2 + \
        sqrt(10)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/5 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1))) == \
        sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 - \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0))) == \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/3 - \
        JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/3 + \
        2*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 + \
        sqrt(5)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1))) == \
        2*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/3 + \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/6 + \
        sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 + \
        2*sqrt(10)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1))) == \
        sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/2 - \
        sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 - \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0))) == \
        sqrt(6)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, S.Half)) )/6 - \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/6 - \
        JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/3 + \
        sqrt(3)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 - \
        JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 + \
        sqrt(5)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1))) == \
        sqrt(3)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, S.Half)) )/3 - \
        JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/3 + \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/6 + \
        sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 - \
        sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 + \
        2*sqrt(10)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1))) == \
        -sqrt(3)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, S.Half)) )/3 - \
        JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/3 + \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/6 + \
        sqrt(6)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 + \
        sqrt(2)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 - \
        2*sqrt(10)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0))) == \
        -sqrt(6)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, S.Half)) )/6 - \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/6 - \
        JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/3 + \
        sqrt(3)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 + \
        JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 - \
        sqrt(5)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1))) == \
        sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/2 + \
        sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 + \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1))) == \
        -sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/2 - \
        sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 - \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0))) == \
        -sqrt(6)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, S.Half)) )/6 - \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/6 - \
        JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/3 - \
        sqrt(3)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 - \
        JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 + \
        sqrt(5)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1))) == \
        -sqrt(3)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, S.Half)) )/3 - \
        JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/3 + \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/6 - \
        sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 - \
        sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 + \
        2*sqrt(10)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1))) == \
        sqrt(3)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, S.Half)) )/3 - \
        JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/3 + \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/6 - \
        sqrt(6)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 + \
        sqrt(2)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 - \
        2*sqrt(10)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0))) == \
        sqrt(6)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, S.Half)) )/6 - \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/6 - \
        JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/3 - \
        sqrt(3)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 + \
        JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 - \
        sqrt(5)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1))) == \
        -sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/2 + \
        sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/6 + \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1))) == \
        2*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/3 + \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/6 - \
        sqrt(2)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 - \
        2*sqrt(10)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0))) == \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, S.Half)) )/3 - \
        JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/3 - \
        2*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 - \
        sqrt(5)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1))) == \
        -sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, S.Half), (1, 4, Rational(3, 2))) )/3 + \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1))) == \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, S.Half)) )/2 - \
        sqrt(10)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/5 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0))) == \
        -sqrt(15)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(3, 2))) )/5 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(-3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1))) == \
        JzKetCoupled(Rational(5, 2), Rational(-5, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (1, 3, Rational(3, 2)), (1, 4, Rational(5, 2))) )
    # Couple j1 to j2, j3 to j4
    # j1=1/2, j2=1/2, j3=1/2, j4=1/2
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)), ((1, 2), (3, 4), (1, 3)) ) == \
        JzKetCoupled(2, 2, (S(
            1)/2, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(2)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 0), (1, 3, 1)) )/2 + \
        JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(2, 1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(2)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 0), (1, 3, 1)) )/2 + \
        JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(2, 1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 0)) )/3 + \
        sqrt(2)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 1)) )/2 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S.Half, S.Half, S.One/
             2), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/6
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(2)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 1), (1, 3, 1)) )/2 - \
        JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(2, 1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))), ((1, 2), (3, 4), (1, 3)) ) == \
        JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 0), (1, 3, 0)) )/2 - \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 0)) )/6 + \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 0), (1, 3, 1)) )/2 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S.Half, S.Half, S.One/
             2), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/6
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)), ((1, 2), (3, 4), (1, 3)) ) == \
        -JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 0), (1, 3, 0)) )/2 - \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 0)) )/6 + \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 1), (1, 3, 1)) )/2 - \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 0), (1, 3, 1)) )/2 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S.Half, S.Half, S.One/
             2), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/6
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(2)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(2, -1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(2)*JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 1), (1, 3, 1)) )/2 - \
        JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(2, 1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))), ((1, 2), (3, 4), (1, 3)) ) == \
        -JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 0), (1, 3, 0)) )/2 - \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 0)) )/6 - \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 0), (1, 3, 1)) )/2 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S.Half, S.Half, S.One/
             2), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/6
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)), ((1, 2), (3, 4), (1, 3)) ) == \
        JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 0), (1, 3, 0)) )/2 - \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 0)) )/6 - \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 1), (1, 3, 1)) )/2 - \
        JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 0), (1, 3, 1)) )/2 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S.Half, S.Half, S.One/
             2), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/6
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(2)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 0), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(2, -1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(3)*JzKetCoupled(0, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 0)) )/3 - \
        sqrt(2)*JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 1)) )/2 + \
        sqrt(6)*JzKetCoupled(2, 0, (S.Half, S.Half, S.Half, S.One/
             2), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/6
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(2)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 0), (1, 3, 1)) )/2 - \
        JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(2, -1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(2)*JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 0), (1, 3, 1)) )/2 - \
        JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 1)) )/2 + \
        JzKetCoupled(2, -1, (S.Half, S(
            1)/2, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))), ((1, 2), (3, 4), (1, 3)) ) == \
        JzKetCoupled(2, -2, (S(
            1)/2, S.Half, S.Half, S.Half), ((1, 2, 1), (3, 4, 1), (1, 3, 2)) )
    # j1=S.Half, S.Half, S.Half, 1
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1)), ((1, 2), (3, 4), (1, 3)) ) == \
        JzKetCoupled(Rational(5, 2), Rational(5, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(3)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 + \
        2*sqrt(15)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1)), ((1, 2), (3, 4), (1, 3)) ) == \
        2*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/3 + \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/6 + \
        sqrt(2)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 + \
        2*sqrt(10)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 + \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/3 + \
        JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/3 - \
        JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 + \
        4*sqrt(5)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/2 + \
        sqrt(10)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/5 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/2 - \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/10 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(6)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, S.Half), (1, 3, S.Half)) )/6 - \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/6 - \
        JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/3 + \
        sqrt(3)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/3 + \
        JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 - \
        sqrt(5)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(3)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, S.Half), (1, 3, S.Half)) )/3 + \
        JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/3 - \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/6 + \
        sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/6 + \
        sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 + \
        sqrt(10)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/30 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(3)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, S.Half), (1, 3, S.Half)) )/3 + \
        JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/3 - \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/6 + \
        sqrt(6)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/6 - \
        sqrt(2)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 - \
        sqrt(10)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/30 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(6)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, S.Half), (1, 3, S.Half)) )/6 - \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/6 - \
        JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/3 + \
        sqrt(3)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/3 - \
        JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 + \
        sqrt(5)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/2 + \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/10 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 1)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/2 - \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/10 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, 0)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(6)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, S.Half), (1, 3, S.Half)) )/6 - \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/6 - \
        JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/3 - \
        sqrt(3)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/3 + \
        JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 - \
        sqrt(5)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(1, -1)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(3)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, S.Half), (1, 3, S.Half)) )/3 + \
        JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/3 - \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/6 - \
        sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/6 + \
        sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 + \
        sqrt(10)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/30 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(3)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, S.Half), (1, 3, S.Half)) )/3 + \
        JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/3 - \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/6 - \
        sqrt(6)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/6 - \
        sqrt(2)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 - \
        sqrt(10)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/30 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(6)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, S.Half), (1, 3, S.Half)) )/6 - \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/6 - \
        JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/3 - \
        sqrt(3)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/3 - \
        JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 + \
        sqrt(5)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 0), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/2 + \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/10 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 1)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(2)*JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/2 - \
        sqrt(10)*JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/5 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, 0)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/3 + \
        JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/3 + \
        JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 - \
        4*sqrt(5)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(1, -1)), ((1, 2), (3, 4), (1, 3)) ) == \
        sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 - \
        sqrt(30)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(5)*JzKetCoupled(Rational(5, 2), Rational(-3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1)), ((1, 2), (3, 4), (1, 3)) ) == \
        2*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, S.Half)) )/3 + \
        sqrt(2)*JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, S.Half)) )/6 - \
        sqrt(2)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 - \
        2*sqrt(10)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/10
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0)), ((1, 2), (3, 4), (1, 3)) ) == \
        -sqrt(3)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, S.Half), (1, 3, Rational(3, 2))) )/3 - \
        2*sqrt(15)*JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(3, 2))) )/15 + \
        sqrt(10)*JzKetCoupled(Rational(5, 2), Rational(-3, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )/5
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1)), ((1, 2), (3, 4), (1, 3)) ) == \
        JzKetCoupled(Rational(5, 2), Rational(-5, 2), (S.Half, S(
            1)/2, S.Half, 1), ((1, 2, 1), (3, 4, Rational(3, 2)), (1, 3, Rational(5, 2))) )

