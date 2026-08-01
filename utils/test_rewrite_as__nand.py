
def test_rewrite_as_Nand():
    expr = (y & z) | (z & ~w)
    assert expr.rewrite(Nand) == ~(~(y & z) & ~(z & ~w))

