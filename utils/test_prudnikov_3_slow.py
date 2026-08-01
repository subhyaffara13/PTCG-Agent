
def test_prudnikov_3_slow():
    # XXX: This is marked as tooslow and hence skipped in CI. None of the
    # individual cases below fails or hangs. Some cases are slow and the loops
    # below generate 280 different cases. Is it really necessary to test all
    # 280 cases here?
    h = S.Half
    for p in [1, 2, 3, 4]:
        for n in [-h, h, 1, 3*h, 2, 5*h, 3, 7*h, 4, 9*h]:
            for m in [1, 3*h, 2, 5*h, 3, 7*h, 4]:
                assert can_do([p, m], [n])

