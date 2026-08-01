
def test_rewrite_as_Nor():
    expr = z & (y | ~w)
    assert expr.rewrite(Nor) == ~(~z | ~(y | ~w))

