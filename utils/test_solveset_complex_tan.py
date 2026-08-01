
def test_solveset_complex_tan():
    s = solveset_complex(tan(x).rewrite(exp), x)
    assert dumeq(s, imageset(Lambda(n, pi*n), S.Integers) - \
        imageset(Lambda(n, pi*n + pi/2), S.Integers))

