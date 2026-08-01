
def test_uncouple_3_coupled_states():
    # Default coupling
    # j1=1/2, j2=1/2, j3=1/2
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(
            S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S(
            1)/2, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S(
            1)/2, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S(
            1)/2, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S(
            1)/2, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S.NegativeOne/
               2), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))) )))
    # j1=1/2, j2=1, j3=1/2
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(S.Half, Rational(-1, 2))) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(S.Half, Rational(-1, 2))) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(S.Half, Rational(-1, 2))) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(S.Half, Rational(-1, 2))) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(S.Half, Rational(-1, 2))) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(
            JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(S.Half, Rational(-1, 2))) )))
    # Coupling j1+j3=j13, j13+j2=j
    # j1=1/2, j2=1/2, j3=1/2
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S.Half), JzKet(
            S.Half, S.Half), JzKet(S.Half, S.Half)), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S.Half), JzKet(
            S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S.Half), JzKet(
            S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S.Half), JzKet(
            S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(
            S.Half, S.Half), JzKet(S.Half, S.Half)), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(
            S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(
            S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(
            S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))), ((1, 3), (1, 2)) )))
    # j1=1/2, j2=1, j3=1/2
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S(
            1)/2), JzKet(1, 1), JzKet(S.Half, S.Half)), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S(
            1)/2), JzKet(1, 1), JzKet(S.Half, Rational(-1, 2))), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S(
            1)/2), JzKet(1, 0), JzKet(S.Half, S.Half)), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S(
            1)/2), JzKet(1, 0), JzKet(S.Half, Rational(-1, 2))), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S(
            1)/2), JzKet(1, -1), JzKet(S.Half, S.Half)), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S(
            1)/2), JzKet(1, -1), JzKet(S.Half, Rational(-1, 2))), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S(
            -1)/2), JzKet(1, 1), JzKet(S.Half, S.Half)), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S(
            -1)/2), JzKet(1, 1), JzKet(S.Half, Rational(-1, 2))), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S(
            -1)/2), JzKet(1, 0), JzKet(S.Half, S.Half)), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S(
            -1)/2), JzKet(1, 0), JzKet(S.Half, Rational(-1, 2))), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S(
            -1)/2), JzKet(1, -1), JzKet(S.Half, S.Half)), ((1, 3), (1, 2)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple( TensorProduct(JzKet(S.Half, S.NegativeOne/
               2), JzKet(1, -1), JzKet(S.Half, Rational(-1, 2))), ((1, 3), (1, 2)) )))

