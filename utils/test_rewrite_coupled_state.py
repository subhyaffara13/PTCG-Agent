
def test_rewrite_coupled_state():
    # Numerical
    assert JyKetCoupled(0, 0, (S.Half, S.Half)).rewrite('Jx') == \
        JxKetCoupled(0, 0, (S.Half, S.Half))
    assert JyKetCoupled(1, 1, (S.Half, S.Half)).rewrite('Jx') == \
        -I*JxKetCoupled(1, 1, (S.Half, S.Half))
    assert JyKetCoupled(1, 0, (S.Half, S.Half)).rewrite('Jx') == \
        JxKetCoupled(1, 0, (S.Half, S.Half))
    assert JyKetCoupled(1, -1, (S.Half, S.Half)).rewrite('Jx') == \
        I*JxKetCoupled(1, -1, (S.Half, S.Half))
    assert JzKetCoupled(0, 0, (S.Half, S.Half)).rewrite('Jx') == \
        JxKetCoupled(0, 0, (S.Half, S.Half))
    assert JzKetCoupled(1, 1, (S.Half, S.Half)).rewrite('Jx') == \
        JxKetCoupled(1, 1, (S.Half, S.Half))/2 - sqrt(2)*JxKetCoupled(1, 0, (
            S.Half, S.Half))/2 + JxKetCoupled(1, -1, (S.Half, S.Half))/2
    assert JzKetCoupled(1, 0, (S.Half, S.Half)).rewrite('Jx') == \
        sqrt(2)*JxKetCoupled(1, 1, (S(
            1)/2, S.Half))/2 - sqrt(2)*JxKetCoupled(1, -1, (S.Half, S.Half))/2
    assert JzKetCoupled(1, -1, (S.Half, S.Half)).rewrite('Jx') == \
        JxKetCoupled(1, 1, (S.Half, S.Half))/2 + sqrt(2)*JxKetCoupled(1, 0, (
            S.Half, S.Half))/2 + JxKetCoupled(1, -1, (S.Half, S.Half))/2
    assert JxKetCoupled(0, 0, (S.Half, S.Half)).rewrite('Jy') == \
        JyKetCoupled(0, 0, (S.Half, S.Half))
    assert JxKetCoupled(1, 1, (S.Half, S.Half)).rewrite('Jy') == \
        I*JyKetCoupled(1, 1, (S.Half, S.Half))
    assert JxKetCoupled(1, 0, (S.Half, S.Half)).rewrite('Jy') == \
        JyKetCoupled(1, 0, (S.Half, S.Half))
    assert JxKetCoupled(1, -1, (S.Half, S.Half)).rewrite('Jy') == \
        -I*JyKetCoupled(1, -1, (S.Half, S.Half))
    assert JzKetCoupled(0, 0, (S.Half, S.Half)).rewrite('Jy') == \
        JyKetCoupled(0, 0, (S.Half, S.Half))
    assert JzKetCoupled(1, 1, (S.Half, S.Half)).rewrite('Jy') == \
        JyKetCoupled(1, 1, (S.Half, S.Half))/2 - I*sqrt(2)*JyKetCoupled(1, 0, (
            S.Half, S.Half))/2 - JyKetCoupled(1, -1, (S.Half, S.Half))/2
    assert JzKetCoupled(1, 0, (S.Half, S.Half)).rewrite('Jy') == \
        -I*sqrt(2)*JyKetCoupled(1, 1, (S.Half, S.Half))/2 - I*sqrt(
            2)*JyKetCoupled(1, -1, (S.Half, S.Half))/2
    assert JzKetCoupled(1, -1, (S.Half, S.Half)).rewrite('Jy') == \
        -JyKetCoupled(1, 1, (S.Half, S.Half))/2 - I*sqrt(2)*JyKetCoupled(1, 0, (S.Half, S.Half))/2 + JyKetCoupled(1, -1, (S.Half, S.Half))/2
    assert JxKetCoupled(0, 0, (S.Half, S.Half)).rewrite('Jz') == \
        JzKetCoupled(0, 0, (S.Half, S.Half))
    assert JxKetCoupled(1, 1, (S.Half, S.Half)).rewrite('Jz') == \
        JzKetCoupled(1, 1, (S.Half, S.Half))/2 + sqrt(2)*JzKetCoupled(1, 0, (
            S.Half, S.Half))/2 + JzKetCoupled(1, -1, (S.Half, S.Half))/2
    assert JxKetCoupled(1, 0, (S.Half, S.Half)).rewrite('Jz') == \
        -sqrt(2)*JzKetCoupled(1, 1, (S(
            1)/2, S.Half))/2 + sqrt(2)*JzKetCoupled(1, -1, (S.Half, S.Half))/2
    assert JxKetCoupled(1, -1, (S.Half, S.Half)).rewrite('Jz') == \
        JzKetCoupled(1, 1, (S.Half, S.Half))/2 - sqrt(2)*JzKetCoupled(1, 0, (
            S.Half, S.Half))/2 + JzKetCoupled(1, -1, (S.Half, S.Half))/2
    assert JyKetCoupled(0, 0, (S.Half, S.Half)).rewrite('Jz') == \
        JzKetCoupled(0, 0, (S.Half, S.Half))
    assert JyKetCoupled(1, 1, (S.Half, S.Half)).rewrite('Jz') == \
        JzKetCoupled(1, 1, (S.Half, S.Half))/2 + I*sqrt(2)*JzKetCoupled(1, 0, (
            S.Half, S.Half))/2 - JzKetCoupled(1, -1, (S.Half, S.Half))/2
    assert JyKetCoupled(1, 0, (S.Half, S.Half)).rewrite('Jz') == \
        I*sqrt(2)*JzKetCoupled(1, 1, (S.Half, S.Half))/2 + I*sqrt(
            2)*JzKetCoupled(1, -1, (S.Half, S.Half))/2
    assert JyKetCoupled(1, -1, (S.Half, S.Half)).rewrite('Jz') == \
        -JzKetCoupled(1, 1, (S.Half, S.Half))/2 + I*sqrt(2)*JzKetCoupled(1, 0, (S.Half, S.Half))/2 + JzKetCoupled(1, -1, (S.Half, S.Half))/2
    # Symbolic
    assert JyKetCoupled(j, m, (j1, j2)).rewrite('Jx') == \
        Sum(WignerD(j, mi, m, 0, 0, pi/2) * JxKetCoupled(j, mi, (
            j1, j2)), (mi, -j, j))
    assert JzKetCoupled(j, m, (j1, j2)).rewrite('Jx') == \
        Sum(WignerD(j, mi, m, 0, pi*Rational(3, 2), 0) * JxKetCoupled(j, mi, (
            j1, j2)), (mi, -j, j))
    assert JxKetCoupled(j, m, (j1, j2)).rewrite('Jy') == \
        Sum(WignerD(j, mi, m, pi*Rational(3, 2), 0, 0) * JyKetCoupled(j, mi, (
            j1, j2)), (mi, -j, j))
    assert JzKetCoupled(j, m, (j1, j2)).rewrite('Jy') == \
        Sum(WignerD(j, mi, m, pi*Rational(3, 2), pi/2, pi/2) * JyKetCoupled(j,
            mi, (j1, j2)), (mi, -j, j))
    assert JxKetCoupled(j, m, (j1, j2)).rewrite('Jz') == \
        Sum(WignerD(j, mi, m, 0, pi/2, 0) * JzKetCoupled(j, mi, (
            j1, j2)), (mi, -j, j))
    assert JyKetCoupled(j, m, (j1, j2)).rewrite('Jz') == \
        Sum(WignerD(j, mi, m, pi*Rational(3, 2), -pi/2, pi/2) * JzKetCoupled(
            j, mi, (j1, j2)), (mi, -j, j))

