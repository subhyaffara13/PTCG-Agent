
def test_rel_queries():
    assert ask(Q.lt(x, 2) & Q.gt(x, 3)) is False
    assert ask(Q.positive(x - z), (x > y) & (y > z)) is True
    assert ask(x + y > 2, (x < 0) & (y <0)) is False
    assert ask(x > z, (x > y) & (y > z)) is True

