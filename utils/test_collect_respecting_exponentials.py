
def test_collect_respecting_exponentials():
    # If this test passes, lines 1306-1311 (at the time of this commit)
    # of sympy/solvers/ode.py should be removed.
    sol = 1 + exp(x/2)
    assert sol == collect( sol, exp(x/3))

