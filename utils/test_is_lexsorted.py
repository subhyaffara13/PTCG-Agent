
def test_is_lexsorted():
    failure = [
        np.array(
            ([3] * 32) + ([2] * 32) + ([1] * 32) + ([0] * 32),
            dtype="int64",
        ),
        np.array(
            list(range(31))[::-1] * 4,
            dtype="int64",
        ),
    ]

    assert not libalgos.is_lexsorted(failure)

