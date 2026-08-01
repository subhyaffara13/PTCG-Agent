
def test_inf():
    assert solve(1 - oo*x) == []
    assert solve(oo*x, x) == []
    assert solve(oo*x - oo, x) == []


def test_inf(engine, parser):
    s = "inf + 1"
    expected = np.inf
    result = pd.eval(s, engine=engine, parser=parser)
    assert result == expected

