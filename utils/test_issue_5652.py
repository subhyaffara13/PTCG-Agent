
def test_issue_5652():
    assert simplify(E + exp(-E)) == exp(-E) + E
    n = symbols('n', commutative=False)
    assert simplify(n + n**(-n)) == n + n**(-n)

