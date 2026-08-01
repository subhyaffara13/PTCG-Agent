
def test_heurisch_complex_erf_issue_26338():
    r = symbols('r', real=True)
    a = sqrt(pi)*erf((1 + I)/2)/2
    assert integrate(exp(-I*r**2/2), (r, 0, 1)) == a - I*a

    a = exp(-x**2/(2*(2 - I)**2))
    assert heurisch(a, x, hints=[]) is None  # None, not a wrong soln
    a = exp(-r**2/(2*(2 - I)**2))
    assert heurisch(a, r, hints=[]) is None
    a = sqrt(pi)*erf((1 + I)/2)/2
    assert integrate(exp(-I*x**2/2), (x, 0, 1)) == a - I*a

