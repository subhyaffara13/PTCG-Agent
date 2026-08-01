
def test_diop_general_sum_of_squares_quick():
    for i in range(3, 10):
        assert check_solutions(sum(i**2 for i in symbols(':%i' % i)) - i)

    assert diop_general_sum_of_squares(x**2 + y**2 - 2) is None
    assert diop_general_sum_of_squares(x**2 + y**2 + z**2 + 2) == set()
    eq = x**2 + y**2 + z**2 - (1 + 4 + 9)
    assert diop_general_sum_of_squares(eq) == \
           {(1, 2, 3)}
    eq = u**2 + v**2 + x**2 + y**2 + z**2 - 1313
    assert len(diop_general_sum_of_squares(eq, 3)) == 3
    # issue 11016
    var = symbols(':5') + (symbols('6', negative=True),)
    eq = Add(*[i**2 for i in var]) - 112

    base_soln = {(0, 1, 1, 5, 6, -7), (1, 1, 1, 3, 6, -8), (2, 3, 3, 4, 5, -7), (0, 1, 1, 1, 3, -10),
                 (0, 0, 4, 4, 4, -8), (1, 2, 3, 3, 5, -8), (0, 1, 2, 3, 7, -7), (2, 2, 4, 4, 6, -6),
                 (1, 1, 3, 4, 6, -7), (0, 2, 3, 3, 3, -9), (0, 0, 2, 2, 2, -10), (1, 1, 2, 3, 4, -9),
                 (0, 1, 1, 2, 5, -9), (0, 0, 2, 6, 6, -6), (1, 3, 4, 5, 5, -6), (0, 2, 2, 2, 6, -8),
                 (0, 3, 3, 3, 6, -7), (0, 2, 3, 5, 5, -7), (0, 1, 5, 5, 5, -6)}
    assert diophantine(eq) == base_soln
    assert len(diophantine(eq, permute=True)) == 196800

    # handle negated squares with signsimp
    assert diophantine(12 - x**2 - y**2 - z**2) == {(2, 2, 2)}
    # diophantine handles simplification, so classify_diop should
    # not have to look for additional patterns that are removed
    # by diophantine
    eq = a**2 + b**2 + c**2 + d**2 - 4
    raises(NotImplementedError, lambda: classify_diop(-eq))

