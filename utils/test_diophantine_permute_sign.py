
def test_diophantine_permute_sign():
    from sympy.abc import a, b, c, d, e
    eq = a**4 + b**4 - (2**4 + 3**4)
    base_sol = {(2, 3)}
    assert diophantine(eq) == base_sol
    complete_soln = set(signed_permutations(base_sol.pop()))
    assert diophantine(eq, permute=True) == complete_soln

    eq = a**2 + b**2 + c**2 + d**2 + e**2 - 234
    assert len(diophantine(eq)) == 35
    assert len(diophantine(eq, permute=True)) == 62000
    soln = {(-1, -1), (-1, 2), (1, -2), (1, 1)}
    assert diophantine(10*x**2 + 12*x*y + 12*y**2 - 34, permute=True) == soln

