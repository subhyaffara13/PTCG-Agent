
def test_solveset_complex_exp():
    assert dumeq(solveset_complex(exp(x) - 1, x),
        imageset(Lambda(n, I*2*n*pi), S.Integers))
    assert dumeq(solveset_complex(exp(x) - I, x),
        imageset(Lambda(n, I*(2*n*pi + pi/2)), S.Integers))
    assert solveset_complex(1/exp(x), x) == S.EmptySet
    assert dumeq(solveset_complex(sinh(x).rewrite(exp), x),
        imageset(Lambda(n, n*pi*I), S.Integers))

