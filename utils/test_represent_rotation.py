
def test_represent_rotation():
    assert represent(Rotation(0, pi/2, 0)) == \
        Matrix(
            [[WignerD(
                S(
                    1)/2, S(
                        1)/2, S(
                            1)/2, 0, pi/2, 0), WignerD(
                                S.Half, S.Half, Rational(-1, 2), 0, pi/2, 0)],
                [WignerD(S.Half, Rational(-1, 2), S.Half, 0, pi/2, 0), WignerD(S.Half, Rational(-1, 2), Rational(-1, 2), 0, pi/2, 0)]])
    assert represent(Rotation(0, pi/2, 0), doit=True) == \
        Matrix([[sqrt(2)/2, -sqrt(2)/2],
                [sqrt(2)/2, sqrt(2)/2]])

