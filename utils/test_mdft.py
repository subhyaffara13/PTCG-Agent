
def test_mdft():
    with warns_deprecated_sympy():
        assert mdft(1) == Matrix([[1]])
    with warns_deprecated_sympy():
        assert mdft(2) == 1/sqrt(2)*Matrix([[1,1],[1,-1]])
    with warns_deprecated_sympy():
        assert mdft(4) == Matrix([[S.Half,  S.Half,  S.Half, S.Half],
                                  [S.Half, -I/2, Rational(-1,2),  I/2],
                                  [S.Half, Rational(-1,2),  S.Half, Rational(-1,2)],
                                  [S.Half,  I/2, Rational(-1,2), -I/2]])

