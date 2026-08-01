
def test_substitution_incorrect():
    # the solutions in the following two tests are incorrect. The
    # correct result is EmptySet in both cases.
    assert substitution([h - 1, k - 1, f - 2, f - 4, -2 * k],
                        [h, k, f]) == {(1, 1, f)}
    assert substitution([x + y + z, S.One, S.One, S.One], [x, y, z]) == \
                        {(-y - z, y, z)}

    # the correct result in the test below is {(-I, I, I, -I),
    # (I, -I, -I, I)}
    assert substitution([a - d, b + d, c + d, d**2 + 1], [a, b, c, d]) == \
                        {(d, -d, -d, d)}

    # the result in the test below is incomplete. The complete result
    # is {(0, b), (log(2), 2)}
    assert substitution([a*(a - log(b)), a*(b - 2)], [a, b]) == \
           {(0, b)}

    # The system in the test below is zero-dimensional, so the result
    # should have no free symbols
    assert substitution([-k*y + 6*x - 4*y, -81*k + 49*y**2 - 270,
                         -3*k*z + k + z**3, k**2 - 2*k + 4],
                        [x, y, z, k]).free_symbols == {z}

