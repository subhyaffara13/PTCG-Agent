
def test_issue_9824():
    assert dumeq(solveset(sin(x)**2 - 2*sin(x) + 1, x), ImageSet(Lambda(n, 2*n*pi + pi/2), S.Integers))
    assert dumeq(solveset(cos(x)**2 - 2*cos(x) + 1, x), ImageSet(Lambda(n, 2*n*pi), S.Integers))

