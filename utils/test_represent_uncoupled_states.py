
def test_represent_uncoupled_states():
    # Jx basis
    assert represent(TensorProduct(JxKet(S.Half, S.Half), JxKet(S.Half, S.Half)), basis=Jx) == \
        Matrix([1, 0, 0, 0])
    assert represent(TensorProduct(JxKet(S.Half, S.Half), JxKet(S.Half, Rational(-1, 2))), basis=Jx) == \
        Matrix([0, 1, 0, 0])
    assert represent(TensorProduct(JxKet(S.Half, Rational(-1, 2)), JxKet(S.Half, S.Half)), basis=Jx) == \
        Matrix([0, 0, 1, 0])
    assert represent(TensorProduct(JxKet(S.Half, Rational(-1, 2)), JxKet(S.Half, Rational(-1, 2))), basis=Jx) == \
        Matrix([0, 0, 0, 1])
    assert represent(TensorProduct(JyKet(S.Half, S.Half), JyKet(S.Half, S.Half)), basis=Jx) == \
        Matrix([-I, 0, 0, 0])
    assert represent(TensorProduct(JyKet(S.Half, S.Half), JyKet(S.Half, Rational(-1, 2))), basis=Jx) == \
        Matrix([0, 1, 0, 0])
    assert represent(TensorProduct(JyKet(S.Half, Rational(-1, 2)), JyKet(S.Half, S.Half)), basis=Jx) == \
        Matrix([0, 0, 1, 0])
    assert represent(TensorProduct(JyKet(S.Half, Rational(-1, 2)), JyKet(S.Half, Rational(-1, 2))), basis=Jx) == \
        Matrix([0, 0, 0, I])
    assert represent(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)), basis=Jx) == \
        Matrix([S.Half, Rational(-1, 2), Rational(-1, 2), S.Half])
    assert represent(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))), basis=Jx) == \
        Matrix([S.Half, S.Half, Rational(-1, 2), Rational(-1, 2)])
    assert represent(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)), basis=Jx) == \
        Matrix([S.Half, Rational(-1, 2), S.Half, Rational(-1, 2)])
    assert represent(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))), basis=Jx) == \
        Matrix([S.Half, S.Half, S.Half, S.Half])
    # Jy basis
    assert represent(TensorProduct(JxKet(S.Half, S.Half), JxKet(S.Half, S.Half)), basis=Jy) == \
        Matrix([I, 0, 0, 0])
    assert represent(TensorProduct(JxKet(S.Half, S.Half), JxKet(S.Half, Rational(-1, 2))), basis=Jy) == \
        Matrix([0, 1, 0, 0])
    assert represent(TensorProduct(JxKet(S.Half, Rational(-1, 2)), JxKet(S.Half, S.Half)), basis=Jy) == \
        Matrix([0, 0, 1, 0])
    assert represent(TensorProduct(JxKet(S.Half, Rational(-1, 2)), JxKet(S.Half, Rational(-1, 2))), basis=Jy) == \
        Matrix([0, 0, 0, -I])
    assert represent(TensorProduct(JyKet(S.Half, S.Half), JyKet(S.Half, S.Half)), basis=Jy) == \
        Matrix([1, 0, 0, 0])
    assert represent(TensorProduct(JyKet(S.Half, S.Half), JyKet(S.Half, Rational(-1, 2))), basis=Jy) == \
        Matrix([0, 1, 0, 0])
    assert represent(TensorProduct(JyKet(S.Half, Rational(-1, 2)), JyKet(S.Half, S.Half)), basis=Jy) == \
        Matrix([0, 0, 1, 0])
    assert represent(TensorProduct(JyKet(S.Half, Rational(-1, 2)), JyKet(S.Half, Rational(-1, 2))), basis=Jy) == \
        Matrix([0, 0, 0, 1])
    assert represent(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)), basis=Jy) == \
        Matrix([S.Half, -I/2, -I/2, Rational(-1, 2)])
    assert represent(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))), basis=Jy) == \
        Matrix([-I/2, S.Half, Rational(-1, 2), -I/2])
    assert represent(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)), basis=Jy) == \
        Matrix([-I/2, Rational(-1, 2), S.Half, -I/2])
    assert represent(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))), basis=Jy) == \
        Matrix([Rational(-1, 2), -I/2, -I/2, S.Half])
    # Jz basis
    assert represent(TensorProduct(JxKet(S.Half, S.Half), JxKet(S.Half, S.Half)), basis=Jz) == \
        Matrix([S.Half, S.Half, S.Half, S.Half])
    assert represent(TensorProduct(JxKet(S.Half, S.Half), JxKet(S.Half, Rational(-1, 2))), basis=Jz) == \
        Matrix([Rational(-1, 2), S.Half, Rational(-1, 2), S.Half])
    assert represent(TensorProduct(JxKet(S.Half, Rational(-1, 2)), JxKet(S.Half, S.Half)), basis=Jz) == \
        Matrix([Rational(-1, 2), Rational(-1, 2), S.Half, S.Half])
    assert represent(TensorProduct(JxKet(S.Half, Rational(-1, 2)), JxKet(S.Half, Rational(-1, 2))), basis=Jz) == \
        Matrix([S.Half, Rational(-1, 2), Rational(-1, 2), S.Half])
    assert represent(TensorProduct(JyKet(S.Half, S.Half), JyKet(S.Half, S.Half)), basis=Jz) == \
        Matrix([S.Half, I/2, I/2, Rational(-1, 2)])
    assert represent(TensorProduct(JyKet(S.Half, S.Half), JyKet(S.Half, Rational(-1, 2))), basis=Jz) == \
        Matrix([I/2, S.Half, Rational(-1, 2), I/2])
    assert represent(TensorProduct(JyKet(S.Half, Rational(-1, 2)), JyKet(S.Half, S.Half)), basis=Jz) == \
        Matrix([I/2, Rational(-1, 2), S.Half, I/2])
    assert represent(TensorProduct(JyKet(S.Half, Rational(-1, 2)), JyKet(S.Half, Rational(-1, 2))), basis=Jz) == \
        Matrix([Rational(-1, 2), I/2, I/2, S.Half])
    assert represent(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, S.Half)), basis=Jz) == \
        Matrix([1, 0, 0, 0])
    assert represent(TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))), basis=Jz) == \
        Matrix([0, 1, 0, 0])
    assert represent(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, S.Half)), basis=Jz) == \
        Matrix([0, 0, 1, 0])
    assert represent(TensorProduct(JzKet(S.Half, Rational(-1, 2)), JzKet(S.Half, Rational(-1, 2))), basis=Jz) == \
        Matrix([0, 0, 0, 1])

