
def test_rewrite_Bra():
    # Numerical
    assert JxBra(1, 1).rewrite('Jy') == -I*JyBra(1, 1)
    assert JxBra(1, 0).rewrite('Jy') == JyBra(1, 0)
    assert JxBra(1, -1).rewrite('Jy') == I*JyBra(1, -1)
    assert JxBra(1, 1).rewrite(
        'Jz') == JzBra(1, 1)/2 + JzBra(1, 0)/sqrt(2) + JzBra(1, -1)/2
    assert JxBra(
        1, 0).rewrite('Jz') == -sqrt(2)*JzBra(1, 1)/2 + sqrt(2)*JzBra(1, -1)/2
    assert JxBra(1, -1).rewrite(
        'Jz') == JzBra(1, 1)/2 - JzBra(1, 0)/sqrt(2) + JzBra(1, -1)/2
    assert JyBra(1, 1).rewrite('Jx') == I*JxBra(1, 1)
    assert JyBra(1, 0).rewrite('Jx') == JxBra(1, 0)
    assert JyBra(1, -1).rewrite('Jx') == -I*JxBra(1, -1)
    assert JyBra(1, 1).rewrite(
        'Jz') == JzBra(1, 1)/2 - sqrt(2)*I*JzBra(1, 0)/2 - JzBra(1, -1)/2
    assert JyBra(1, 0).rewrite(
        'Jz') == -sqrt(2)*I*JzBra(1, 1)/2 - sqrt(2)*I*JzBra(1, -1)/2
    assert JyBra(1, -1).rewrite(
        'Jz') == -JzBra(1, 1)/2 - sqrt(2)*I*JzBra(1, 0)/2 + JzBra(1, -1)/2
    assert JzBra(1, 1).rewrite(
        'Jx') == JxBra(1, 1)/2 - sqrt(2)*JxBra(1, 0)/2 + JxBra(1, -1)/2
    assert JzBra(
        1, 0).rewrite('Jx') == sqrt(2)*JxBra(1, 1)/2 - sqrt(2)*JxBra(1, -1)/2
    assert JzBra(1, -1).rewrite(
        'Jx') == JxBra(1, 1)/2 + sqrt(2)*JxBra(1, 0)/2 + JxBra(1, -1)/2
    assert JzBra(1, 1).rewrite(
        'Jy') == JyBra(1, 1)/2 + sqrt(2)*I*JyBra(1, 0)/2 - JyBra(1, -1)/2
    assert JzBra(1, 0).rewrite(
        'Jy') == sqrt(2)*I*JyBra(1, 1)/2 + sqrt(2)*I*JyBra(1, -1)/2
    assert JzBra(1, -1).rewrite(
        'Jy') == -JyBra(1, 1)/2 + sqrt(2)*I*JyBra(1, 0)/2 + JyBra(1, -1)/2
    # Symbolic
    assert JxBra(j, m).rewrite('Jy') == Sum(
        WignerD(j, mi, m, pi*Rational(3, 2), 0, 0) * JyBra(j, mi), (mi, -j, j))
    assert JxBra(j, m).rewrite('Jz') == Sum(
        WignerD(j, mi, m, 0, pi/2, 0) * JzBra(j, mi), (mi, -j, j))
    assert JyBra(j, m).rewrite('Jx') == Sum(
        WignerD(j, mi, m, 0, 0, pi/2) * JxBra(j, mi), (mi, -j, j))
    assert JyBra(j, m).rewrite('Jz') == Sum(
        WignerD(j, mi, m, pi*Rational(3, 2), -pi/2, pi/2) * JzBra(j, mi), (mi, -j, j))
    assert JzBra(j, m).rewrite('Jx') == Sum(
        WignerD(j, mi, m, 0, pi*Rational(3, 2), 0) * JxBra(j, mi), (mi, -j, j))
    assert JzBra(j, m).rewrite('Jy') == Sum(
        WignerD(j, mi, m, pi*Rational(3, 2), pi/2, pi/2) * JyBra(j, mi), (mi, -j, j))

