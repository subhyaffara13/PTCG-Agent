
def test_dft2():
    assert DFT(1).as_explicit() == Matrix([[1]])
    assert DFT(2).as_explicit() == 1/sqrt(2)*Matrix([[1,1],[1,-1]])
    assert DFT(4).as_explicit() == Matrix([[S.Half,  S.Half,  S.Half, S.Half],
                                           [S.Half, -I/2, Rational(-1,2),  I/2],
                                           [S.Half, Rational(-1,2),  S.Half, Rational(-1,2)],
                                           [S.Half,  I/2, Rational(-1,2), -I/2]])

