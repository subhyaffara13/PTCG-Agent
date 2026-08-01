
def test_precomputed_cases():
    for a, side, expected_u, expected_p in precomputed_cases:
        check_precomputed_polar(a, side, expected_u, expected_p)

