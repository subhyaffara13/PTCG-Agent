
def test_C18():
    assert simplify((sqrt(-2 + sqrt(-5)) * sqrt(-2 - sqrt(-5))).expand(complex=True)) == 3

