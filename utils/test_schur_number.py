
def test_schur_number():
    first_known_schur_numbers = {1: 1, 2: 4, 3: 13, 4: 44, 5: 160}
    for k in first_known_schur_numbers:
        assert SchurNumber(k) == first_known_schur_numbers[k]

    assert SchurNumber(S.Infinity) == S.Infinity
    assert SchurNumber(0) == 0
    raises(ValueError, lambda: SchurNumber(0.5))

    n = symbols("n")
    assert SchurNumber(n).lower_bound() == 3**n/2 - Rational(1, 2)
    assert SchurNumber(8).lower_bound() == 5039

