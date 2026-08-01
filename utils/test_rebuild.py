
def test_rebuild():
    expr = Basic.__new__(Add, S(1), S(2))
    assert rebuild(expr) == 3

