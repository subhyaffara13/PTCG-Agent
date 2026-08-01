
def test_factor_sets():
    #
    from random import randint

    def generate_random_system(n_eqs=3, n_factors=2, max_val=10):
        return [
            [randint(0, max_val) for _ in range(randint(1, n_factors))]
            for _ in range(n_eqs)
        ]

    test_cases = [
        [[1, 2], [1, 3]],
        [[1, 2], [3, 4]],
        [[1], [1, 2], [2]],
    ]

    for case in test_cases:
        assert _factor_sets(case) == _factor_sets_slow(case)

    for _ in range(100):
        system = generate_random_system()
        assert _factor_sets(system) == _factor_sets_slow(system)

