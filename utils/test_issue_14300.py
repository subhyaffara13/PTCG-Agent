
def test_issue_14300():
    f = 1 - exp(-18000000*x) - y
    a1 = FiniteSet(-log(-y + 1)/18000000)

    assert solveset(f, x, S.Reals) == \
        Intersection(S.Reals, a1)
    assert dumeq(solveset(f, x),
        ImageSet(Lambda(n, -I*(2*n*pi + arg(-y + 1))/18000000 -
            log(Abs(y - 1))/18000000), S.Integers))

