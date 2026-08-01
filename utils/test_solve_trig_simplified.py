
def test_solve_trig_simplified():
    n = Dummy('n')
    assert dumeq(solveset_real(sin(x), x),
        imageset(Lambda(n, n*pi), S.Integers))

    assert dumeq(solveset_real(cos(x), x),
        imageset(Lambda(n, n*pi + pi/2), S.Integers))

    assert dumeq(solveset_real(cos(x) + sin(x), x),
        imageset(Lambda(n, n*pi - pi/4), S.Integers))

