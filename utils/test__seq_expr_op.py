
def test_SeqExprOp():
    form = SeqFormula(n**2, (n, 0, 10))
    per = SeqPer((1, 2, 3), (m, 5, 10))

    s = SeqExprOp(form, per)
    assert s.gen == (n**2, (1, 2, 3))
    assert s.interval == Interval(5, 10)
    assert s.start == 5
    assert s.stop == 10
    assert s.length == 6
    assert s.variables == (n, m)

