
def test_represent_spin_states():
    # Jx basis
    assert represent(JxKet(S.Half, S.Half), basis=Jx) == Matrix([1, 0])
    assert represent(JxKet(S.Half, Rational(-1, 2)), basis=Jx) == Matrix([0, 1])
    assert represent(JxKet(1, 1), basis=Jx) == Matrix([1, 0, 0])
    assert represent(JxKet(1, 0), basis=Jx) == Matrix([0, 1, 0])
    assert represent(JxKet(1, -1), basis=Jx) == Matrix([0, 0, 1])
    assert represent(
        JyKet(S.Half, S.Half), basis=Jx) == Matrix([exp(-I*pi/4), 0])
    assert represent(
        JyKet(S.Half, Rational(-1, 2)), basis=Jx) == Matrix([0, exp(I*pi/4)])
    assert represent(JyKet(1, 1), basis=Jx) == Matrix([-I, 0, 0])
    assert represent(JyKet(1, 0), basis=Jx) == Matrix([0, 1, 0])
    assert represent(JyKet(1, -1), basis=Jx) == Matrix([0, 0, I])
    assert represent(
        JzKet(S.Half, S.Half), basis=Jx) == sqrt(2)*Matrix([-1, 1])/2
    assert represent(
        JzKet(S.Half, Rational(-1, 2)), basis=Jx) == sqrt(2)*Matrix([-1, -1])/2
    assert represent(JzKet(1, 1), basis=Jx) == Matrix([1, -sqrt(2), 1])/2
    assert represent(JzKet(1, 0), basis=Jx) == sqrt(2)*Matrix([1, 0, -1])/2
    assert represent(JzKet(1, -1), basis=Jx) == Matrix([1, sqrt(2), 1])/2
    # Jy basis
    assert represent(
        JxKet(S.Half, S.Half), basis=Jy) == Matrix([exp(I*pi*Rational(-3, 4)), 0])
    assert represent(
        JxKet(S.Half, Rational(-1, 2)), basis=Jy) == Matrix([0, exp(I*pi*Rational(3, 4))])
    assert represent(JxKet(1, 1), basis=Jy) == Matrix([I, 0, 0])
    assert represent(JxKet(1, 0), basis=Jy) == Matrix([0, 1, 0])
    assert represent(JxKet(1, -1), basis=Jy) == Matrix([0, 0, -I])
    assert represent(JyKet(S.Half, S.Half), basis=Jy) == Matrix([1, 0])
    assert represent(JyKet(S.Half, Rational(-1, 2)), basis=Jy) == Matrix([0, 1])
    assert represent(JyKet(1, 1), basis=Jy) == Matrix([1, 0, 0])
    assert represent(JyKet(1, 0), basis=Jy) == Matrix([0, 1, 0])
    assert represent(JyKet(1, -1), basis=Jy) == Matrix([0, 0, 1])
    assert represent(
        JzKet(S.Half, S.Half), basis=Jy) == sqrt(2)*Matrix([-1, I])/2
    assert represent(
        JzKet(S.Half, Rational(-1, 2)), basis=Jy) == sqrt(2)*Matrix([I, -1])/2
    assert represent(JzKet(1, 1), basis=Jy) == Matrix([1, -I*sqrt(2), -1])/2
    assert represent(
        JzKet(1, 0), basis=Jy) == Matrix([-sqrt(2)*I, 0, -sqrt(2)*I])/2
    assert represent(JzKet(1, -1), basis=Jy) == Matrix([-1, -sqrt(2)*I, 1])/2
    # Jz basis
    assert represent(
        JxKet(S.Half, S.Half), basis=Jz) == sqrt(2)*Matrix([1, 1])/2
    assert represent(
        JxKet(S.Half, Rational(-1, 2)), basis=Jz) == sqrt(2)*Matrix([-1, 1])/2
    assert represent(JxKet(1, 1), basis=Jz) == Matrix([1, sqrt(2), 1])/2
    assert represent(JxKet(1, 0), basis=Jz) == sqrt(2)*Matrix([-1, 0, 1])/2
    assert represent(JxKet(1, -1), basis=Jz) == Matrix([1, -sqrt(2), 1])/2
    assert represent(
        JyKet(S.Half, S.Half), basis=Jz) == sqrt(2)*Matrix([-1, -I])/2
    assert represent(
        JyKet(S.Half, Rational(-1, 2)), basis=Jz) == sqrt(2)*Matrix([-I, -1])/2
    assert represent(JyKet(1, 1), basis=Jz) == Matrix([1, sqrt(2)*I, -1])/2
    assert represent(JyKet(1, 0), basis=Jz) == sqrt(2)*Matrix([I, 0, I])/2
    assert represent(JyKet(1, -1), basis=Jz) == Matrix([-1, sqrt(2)*I, 1])/2
    assert represent(JzKet(S.Half, S.Half), basis=Jz) == Matrix([1, 0])
    assert represent(JzKet(S.Half, Rational(-1, 2)), basis=Jz) == Matrix([0, 1])
    assert represent(JzKet(1, 1), basis=Jz) == Matrix([1, 0, 0])
    assert represent(JzKet(1, 0), basis=Jz) == Matrix([0, 1, 0])
    assert represent(JzKet(1, -1), basis=Jz) == Matrix([0, 0, 1])

