
def test_prudnikov_2():
    h = S.Half
    assert can_do([-h, -h], [h])
    assert can_do([-h, h], [3*h])
    assert can_do([-h, h], [5*h])
    assert can_do([-h, h], [7*h])
    assert can_do([-h, 1], [h])

    for p in [-h, h]:
        for n in [-h, h, 1, 3*h, 2, 5*h, 3, 7*h, 4]:
            for m in [-h, h, 3*h, 5*h, 7*h]:
                assert can_do([p, n], [m])
        for n in [1, 2, 3, 4]:
            for m in [1, 2, 3, 4]:
                assert can_do([p, n], [m])

