
def test_diop_sum_of_even_powers():
    eq = x**4 + y**4 + z**4 - 2673
    assert diop_solve(eq) == {(3, 6, 6), (2, 4, 7)}
    assert diop_general_sum_of_even_powers(eq, 2) == {(3, 6, 6), (2, 4, 7)}
    raises(NotImplementedError, lambda: diop_general_sum_of_even_powers(-eq, 2))
    neg = symbols('neg', negative=True)
    eq = x**4 + y**4 + neg**4 - 2673
    assert diop_general_sum_of_even_powers(eq) == {(-3, 6, 6)}
    assert diophantine(x**4 + y**4 + 2) == set()
    assert diop_general_sum_of_even_powers(x**4 + y**4 - 2, limit=0) == set()

