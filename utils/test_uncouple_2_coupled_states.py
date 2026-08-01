
def test_uncouple_2_coupled_states():
    # j1=1/2, j2=1/2
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple(
            TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)) == \
        expand(uncouple(couple(
            TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple(
            TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))) == \
        expand(uncouple(couple(
            TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))) )))
    # j1=1/2, j2=1
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1)) == \
        expand(uncouple(
            couple( TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 1)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0)) == \
        expand(uncouple(
            couple( TensorProduct(JzKet(S.Half, S.Half), JzKet(1, 0)) )))
    assert TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1)) == \
        expand(uncouple(
            couple( TensorProduct(JzKet(S.Half, S.Half), JzKet(1, -1)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1)) == \
        expand(uncouple(
            couple( TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 1)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0)) == \
        expand(uncouple(
            couple( TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, 0)) )))
    assert TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1)) == \
        expand(uncouple(
            couple( TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(1, -1)) )))
    # j1=1, j2=1
    assert TensorProduct(JzKet(1, 1), JzKet(1, 1)) == \
        expand(uncouple(couple( TensorProduct(JzKet(1, 1), JzKet(1, 1)) )))
    assert TensorProduct(JzKet(1, 1), JzKet(1, 0)) == \
        expand(uncouple(couple( TensorProduct(JzKet(1, 1), JzKet(1, 0)) )))
    assert TensorProduct(JzKet(1, 1), JzKet(1, -1)) == \
        expand(uncouple(couple( TensorProduct(JzKet(1, 1), JzKet(1, -1)) )))
    assert TensorProduct(JzKet(1, 0), JzKet(1, 1)) == \
        expand(uncouple(couple( TensorProduct(JzKet(1, 0), JzKet(1, 1)) )))
    assert TensorProduct(JzKet(1, 0), JzKet(1, 0)) == \
        expand(uncouple(couple( TensorProduct(JzKet(1, 0), JzKet(1, 0)) )))
    assert TensorProduct(JzKet(1, 0), JzKet(1, -1)) == \
        expand(uncouple(couple( TensorProduct(JzKet(1, 0), JzKet(1, -1)) )))
    assert TensorProduct(JzKet(1, -1), JzKet(1, 1)) == \
        expand(uncouple(couple( TensorProduct(JzKet(1, -1), JzKet(1, 1)) )))
    assert TensorProduct(JzKet(1, -1), JzKet(1, 0)) == \
        expand(uncouple(couple( TensorProduct(JzKet(1, -1), JzKet(1, 0)) )))
    assert TensorProduct(JzKet(1, -1), JzKet(1, -1)) == \
        expand(uncouple(couple( TensorProduct(JzKet(1, -1), JzKet(1, -1)) )))

