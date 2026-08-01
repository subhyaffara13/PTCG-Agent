
def test_prudnikov_8():
    h = S.Half

    # 7.12.2
    for ai in [1, 2, 3]:
        for bi in [1, 2, 3]:
            for ci in range(1, ai + 1):
                for di in [h, 1, 3*h, 2, 5*h, 3]:
                    assert can_do([ai, bi], [ci, di])
        for bi in [3*h, 5*h]:
            for ci in [h, 1, 3*h, 2, 5*h, 3]:
                for di in [1, 2, 3]:
                    assert can_do([ai, bi], [ci, di])

    for ai in [-h, h, 3*h, 5*h]:
        for bi in [1, 2, 3]:
            for ci in [h, 1, 3*h, 2, 5*h, 3]:
                for di in [1, 2, 3]:
                    assert can_do([ai, bi], [ci, di])
        for bi in [h, 3*h, 5*h]:
            for ci in [h, 3*h, 5*h, 3]:
                for di in [h, 1, 3*h, 2, 5*h, 3]:
                    if ci <= bi:
                        assert can_do([ai, bi], [ci, di])

