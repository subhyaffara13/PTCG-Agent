
def test_unit_clause():
    A, B, C = symbols('A,B,C')
    assert find_unit_clause([A], {}) == (A, True)
    assert find_unit_clause([A, ~A], {}) == (A, True)  # Wrong ??
    assert find_unit_clause([A | B], {A: True}) == (B, True)
    assert find_unit_clause([A | B], {B: True}) == (A, True)
    assert find_unit_clause(
        [A | B | C, B | ~C, A | ~B], {A: True}) == (B, False)
    assert find_unit_clause([A | B | C, B | ~C, A | B], {A: True}) == (B, True)
    assert find_unit_clause([A | B | C, B | ~C, A ], {}) == (A, True)

