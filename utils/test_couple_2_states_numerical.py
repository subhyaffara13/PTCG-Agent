
def test_couple_2_states_numerical():
    # j1=1/2, j2=1/2
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half))) == \
        JzKetCoupled(1, 1, (S.Half, S.Half))
    assert couple(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)))) == \
        sqrt(2)*JzKetCoupled(0, 0, (S(
            1)/2, S.Half))/2 + sqrt(2)*JzKetCoupled(1, 0, (S.Half, S.Half))/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half))) == \
        -sqrt(2)*JzKetCoupled(0, 0, (S(
            1)/2, S.Half))/2 + sqrt(2)*JzKetCoupled(1, 0, (S.Half, S.Half))/2
    assert couple(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)))) == \
        JzKetCoupled(1, -1, (S.Half, S.Half))
    # j1=1, j2=1/2
    assert couple(TensorProduct(JzKet(1, 1), JzKet(S.Half, S.Half))) == \
        JzKetCoupled(Rational(3, 2), Rational(3, 2), (1, S.Half))
    assert couple(TensorProduct(JzKet(1, 1), JzKet(S.Half, Rational(-1, 2)))) == \
        sqrt(6)*JzKetCoupled(S.Half, S.Half, (1, S.Half))/3 + sqrt(
            3)*JzKetCoupled(Rational(3, 2), S.Half, (1, S.Half))/3
    assert couple(TensorProduct(JzKet(1, 0), JzKet(S.Half, S.Half))) == \
        -sqrt(3)*JzKetCoupled(S.Half, S.Half, (1, S.Half))/3 + \
        sqrt(6)*JzKetCoupled(Rational(3, 2), S.Half, (1, S.Half))/3
    assert couple(TensorProduct(JzKet(1, 0), JzKet(S.Half, Rational(-1, 2)))) == \
        sqrt(3)*JzKetCoupled(S.Half, Rational(-1, 2), (1, S.Half))/3 + \
        sqrt(6)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (1, S.Half))/3
    assert couple(TensorProduct(JzKet(1, -1), JzKet(S.Half, S.Half))) == \
        -sqrt(6)*JzKetCoupled(S.Half, Rational(-1, 2), (1, S(
            1)/2))/3 + sqrt(3)*JzKetCoupled(Rational(3, 2), Rational(-1, 2), (1, S.Half))/3
    assert couple(TensorProduct(JzKet(1, -1), JzKet(S.Half, Rational(-1, 2)))) == \
        JzKetCoupled(Rational(3, 2), Rational(-3, 2), (1, S.Half))
    # j1=1, j2=1
    assert couple(TensorProduct(JzKet(1, 1), JzKet(1, 1))) == \
        JzKetCoupled(2, 2, (1, 1))
    assert couple(TensorProduct(JzKet(1, 1), JzKet(1, 0))) == \
        sqrt(2)*JzKetCoupled(
            1, 1, (1, 1))/2 + sqrt(2)*JzKetCoupled(2, 1, (1, 1))/2
    assert couple(TensorProduct(JzKet(1, 1), JzKet(1, -1))) == \
        sqrt(3)*JzKetCoupled(0, 0, (1, 1))/3 + sqrt(2)*JzKetCoupled(
            1, 0, (1, 1))/2 + sqrt(6)*JzKetCoupled(2, 0, (1, 1))/6
    assert couple(TensorProduct(JzKet(1, 0), JzKet(1, 1))) == \
        -sqrt(2)*JzKetCoupled(
            1, 1, (1, 1))/2 + sqrt(2)*JzKetCoupled(2, 1, (1, 1))/2
    assert couple(TensorProduct(JzKet(1, 0), JzKet(1, 0))) == \
        -sqrt(3)*JzKetCoupled(
            0, 0, (1, 1))/3 + sqrt(6)*JzKetCoupled(2, 0, (1, 1))/3
    assert couple(TensorProduct(JzKet(1, 0), JzKet(1, -1))) == \
        sqrt(2)*JzKetCoupled(
            1, -1, (1, 1))/2 + sqrt(2)*JzKetCoupled(2, -1, (1, 1))/2
    assert couple(TensorProduct(JzKet(1, -1), JzKet(1, 1))) == \
        sqrt(3)*JzKetCoupled(0, 0, (1, 1))/3 - sqrt(2)*JzKetCoupled(
            1, 0, (1, 1))/2 + sqrt(6)*JzKetCoupled(2, 0, (1, 1))/6
    assert couple(TensorProduct(JzKet(1, -1), JzKet(1, 0))) == \
        -sqrt(2)*JzKetCoupled(
            1, -1, (1, 1))/2 + sqrt(2)*JzKetCoupled(2, -1, (1, 1))/2
    assert couple(TensorProduct(JzKet(1, -1), JzKet(1, -1))) == \
        JzKetCoupled(2, -2, (1, 1))
    # j1=3/2, j2=1/2
    assert couple(TensorProduct(JzKet(Rational(3, 2), Rational(3, 2)), JzKet(S.Half, S.Half))) == \
        JzKetCoupled(2, 2, (Rational(3, 2), S.Half))
    assert couple(TensorProduct(JzKet(Rational(3, 2), Rational(3, 2)), JzKet(S.Half, Rational(-1, 2)))) == \
        sqrt(3)*JzKetCoupled(
            1, 1, (Rational(3, 2), S.Half))/2 + JzKetCoupled(2, 1, (Rational(3, 2), S.Half))/2
    assert couple(TensorProduct(JzKet(Rational(3, 2), S.Half), JzKet(S.Half, S.Half))) == \
        -JzKetCoupled(1, 1, (S(
            3)/2, S.Half))/2 + sqrt(3)*JzKetCoupled(2, 1, (Rational(3, 2), S.Half))/2
    assert couple(TensorProduct(JzKet(Rational(3, 2), S.Half), JzKet(S.Half, Rational(-1, 2)))) == \
        sqrt(2)*JzKetCoupled(1, 0, (S(
            3)/2, S.Half))/2 + sqrt(2)*JzKetCoupled(2, 0, (Rational(3, 2), S.Half))/2
    assert couple(TensorProduct(JzKet(Rational(3, 2), Rational(-1, 2)), JzKet(S.Half, S.Half))) == \
        -sqrt(2)*JzKetCoupled(1, 0, (S(
            3)/2, S.Half))/2 + sqrt(2)*JzKetCoupled(2, 0, (Rational(3, 2), S.Half))/2
    assert couple(TensorProduct(JzKet(Rational(3, 2), Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)))) == \
        JzKetCoupled(1, -1, (S(
            3)/2, S.Half))/2 + sqrt(3)*JzKetCoupled(2, -1, (Rational(3, 2), S.Half))/2
    assert couple(TensorProduct(JzKet(Rational(3, 2), Rational(-3, 2)), JzKet(S.Half, S.Half))) == \
        -sqrt(3)*JzKetCoupled(1, -1, (Rational(3, 2), S.Half))/2 + \
        JzKetCoupled(2, -1, (Rational(3, 2), S.Half))/2
    assert couple(TensorProduct(JzKet(Rational(3, 2), Rational(-3, 2)), JzKet(S.Half, Rational(-1, 2)))) == \
        JzKetCoupled(2, -2, (Rational(3, 2), S.Half))

