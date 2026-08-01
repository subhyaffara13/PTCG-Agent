
def test_invalid_partial_derivative_valence():
    raises(ValueError, lambda: PartialDerivative(C(j), D(-j)))
    raises(ValueError, lambda: PartialDerivative(C(-j), D(j)))

