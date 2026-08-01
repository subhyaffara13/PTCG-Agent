
def test_number_operator():
    n = symbols("n")
    o = Bd(0)*B(0)
    e = apply_operators(o*BKet([n]))
    assert e == n*BKet([n])

