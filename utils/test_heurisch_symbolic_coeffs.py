
def test_heurisch_symbolic_coeffs():
    assert heurisch(1/(x + y), x) == log(x + y)
    assert heurisch(1/(x + sqrt(2)), x) == log(x + sqrt(2))
    assert simplify(diff(heurisch(log(x + y + z), y), y)) == log(x + y + z)

