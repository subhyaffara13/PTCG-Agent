
def test_polysys():
    assert set(solve([x**2 + 2/y - 2, x + y - 3], [x, y])) == \
        {(S.One, S(2)), (1 + sqrt(5), 2 - sqrt(5)),
        (1 - sqrt(5), 2 + sqrt(5))}
    assert solve([x**2 + y - 2, x**2 + y]) == []
    # the ordering should be whatever the user requested
    assert solve([x**2 + y - 3, x - y - 4], (x, y)) != solve([x**2 +
                 y - 3, x - y - 4], (y, x))

