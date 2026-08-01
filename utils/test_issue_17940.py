
def test_issue_17940():
    n = Dummy('n')
    k1 = Dummy('k1')
    sol = ImageSet(Lambda(((k1, n),), I*(2*k1*pi + arg(2*n*I*pi + log(5)))
                          + log(Abs(2*n*I*pi + log(5)))),
                   ProductSet(S.Integers, S.Integers))
    assert solveset(exp(exp(x)) - 5, x).dummy_eq(sol)

