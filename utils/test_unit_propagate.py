
def test_unit_propagate():
    A, B, C = symbols('A,B,C')
    assert unit_propagate([A | B], A) == []
    assert unit_propagate([A | B, ~A | C, ~C | B, A], A) == [C, ~C | B, A]

