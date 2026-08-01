
def test_solvify():
    assert solvify(x**2 + 10, x, S.Reals) == []
    assert solvify(x**3 + 1, x, S.Complexes) == [-1, S.Half - sqrt(3)*I/2,
                                                 S.Half + sqrt(3)*I/2]
    assert solvify(log(x), x, S.Reals) == [1]
    assert solvify(cos(x), x, S.Reals) == [pi/2, pi*Rational(3, 2)]
    assert solvify(sin(x) + 1, x, S.Reals) == [pi*Rational(3, 2)]
    raises(NotImplementedError, lambda: solvify(sin(exp(x)), x, S.Complexes))

