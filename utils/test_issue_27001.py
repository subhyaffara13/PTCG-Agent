
def test_issue_27001():
    assert solve((x, x**2), (x, y, z), dict=True) == [{x: 0}]
    s = a1, a2, a3, a4, a5 = symbols('a1:6')
    eqs = [8*a1**4*a2 + 4*a1**2*a2**3 - 8*a1**2*a2*a4 + a2**5/2 - 2*a2**3*a4 +
        8*a2*a3**2 + 2*a2*a4**2 + 8*a2*a5, 12*a1**4 + 6*a1**2*a2**2 -
        8*a1**2*a4 + 3*a2**4/4 - 2*a2**2*a4 + 4*a3**2 + a4**2 + 4*a5, 16*a1**3
        + 4*a1*a2**2 - 8*a1*a4, -8*a1**2*a2 - 2*a2**3 + 4*a2*a4]
    sol = [{a4: 2*a1**2 + a2**2/2, a5: -a3**2}, {a1: 0, a2: 0, a5: -a3**2 - a4**2/4}]
    assert solve(eqs, s, dict=True) == sol
    assert (g:=solve(groebner(eqs, s), dict=True)) == sol, g

