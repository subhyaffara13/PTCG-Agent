
def test_basic_apply():
    n = symbols("n")
    e = B(0)*BKet([n])
    assert apply_operators(e) == sqrt(n)*BKet([n - 1])
    e = Bd(0)*BKet([n])
    assert apply_operators(e) == sqrt(n + 1)*BKet([n + 1])

