
def test_Interval():
    n = (S.NegativeInfinity, 1, 2, S.Infinity)
    for i in range(len(n)):
        for j in range(i + 1, len(n)):
            for l in (True, False):
                for r in (True, False):
                    ival = Interval(n[i], n[j], l, r)
                    assert S(str(ival)) == ival

