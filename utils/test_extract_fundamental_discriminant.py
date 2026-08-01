
def test_extract_fundamental_discriminant():
    # To extract, integer must be 0 or 1 mod 4.
    raises(ValueError, lambda: extract_fundamental_discriminant(2))
    raises(ValueError, lambda: extract_fundamental_discriminant(3))
    # Try many cases, of different forms:
    cases = (
        (0, {}, {0: 1}),
        (1, {}, {}),
        (8, {2: 3}, {}),
        (-8, {2: 3, -1: 1}, {}),
        (12, {2: 2, 3: 1}, {}),
        (36, {}, {2: 1, 3: 1}),
        (45, {5: 1}, {3: 1}),
        (48, {2: 2, 3: 1}, {2: 1}),
        (1125, {5: 1}, {3: 1, 5: 1}),
    )
    for a, D_expected, F_expected in cases:
        D, F = extract_fundamental_discriminant(a)
        assert D == D_expected
        assert F == F_expected

