
def test_polyder(xp):
    cases = [
        ([5], 0, [5]),
        ([5], 1, [0]),
        ([3, 2, 1], 0, [3, 2, 1]),
        ([3, 2, 1], 1, [6, 2]),
        ([3, 2, 1], 2, [6]),
        ([3, 2, 1], 3, [0]),
        ([[3, 2, 1], [5, 6, 7]], 0, [[3, 2, 1], [5, 6, 7]]),
        ([[3, 2, 1], [5, 6, 7]], 1, [[6, 2], [10, 6]]),
        ([[3, 2, 1], [5, 6, 7]], 2, [[6], [10]]),
        ([[3, 2, 1], [5, 6, 7]], 3, [[0], [0]]),
    ]
    for p, m, expected in cases:
        pp = xp.asarray(p)
        ee = xp.asarray(expected)
        check_polyder(
            pp.T if pp.ndim == 2 else pp,
            m,
            ee.T if ee.ndim ==2 else ee,
            xp
        )

