
def test_complex_apply():
    n, m = symbols("n,m")
    o = Bd(0)*B(0)*Bd(1)*B(0)
    e = apply_operators(o*BKet([n, m]))
    answer = sqrt(n)*sqrt(m + 1)*(-1 + n)*BKet([-1 + n, 1 + m])
    assert expand(e) == expand(answer)

