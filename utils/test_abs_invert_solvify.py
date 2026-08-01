
def test_abs_invert_solvify():

    x = Symbol('x',positive=True)
    assert solvify(sin(Abs(x)), x, S.Reals) == [0, pi]
    x = Symbol('x')
    assert solvify(sin(Abs(x)), x, S.Reals) is None

