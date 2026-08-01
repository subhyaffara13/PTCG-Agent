
def test_prudnikov_10():
    # 7.14.2
    h = S.Half
    for p in [-h, h, 1, 3*h, 2, 5*h, 3, 7*h, 4]:
        for m in [1, 2, 3, 4]:
            for n in range(m, 5):
                assert can_do([p], [m, n])

    for p in [1, 2, 3, 4]:
        for n in [h, 3*h, 5*h, 7*h]:
            for m in [1, 2, 3, 4]:
                assert can_do([p], [n, m])

    for p in [3*h, 5*h, 7*h]:
        for m in [h, 1, 2, 5*h, 3, 7*h, 4]:
            assert can_do([p], [h, m])
            assert can_do([p], [3*h, m])

    for m in [h, 1, 2, 5*h, 3, 7*h, 4]:
        assert can_do([7*h], [5*h, m])

    assert can_do([Rational(-1, 2)], [S.Half, S.Half])  # shine-integral shi

