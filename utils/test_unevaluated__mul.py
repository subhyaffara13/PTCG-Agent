
def test_unevaluated_Mul():
    m = [Mul(1, 2, evaluate=False)]
    assert cse(m) == ([], m)

