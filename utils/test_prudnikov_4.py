
def test_prudnikov_4():
    h = S.Half
    for p in [3*h, 5*h, 7*h]:
        for n in [-h, h, 3*h, 5*h, 7*h]:
            for m in [3*h, 2, 5*h, 3, 7*h, 4]:
                assert can_do([p, m], [n])
        for n in [1, 2, 3, 4]:
            for m in [2, 3, 4]:
                assert can_do([p, m], [n])

