
def test_univariate():
    assert diop_solve((x - 1)*(x - 2)**2) == {(1,), (2,)}
    assert diop_solve((x - 1)*(x - 2)) == {(1,), (2,)}

