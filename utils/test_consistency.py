
def test_consistency():
    # Make sure the implementation of digamma for real arguments
    # agrees with the implementation of digamma for complex arguments.

    # It's all poles after -1e16
    x = np.r_[-np.logspace(15, -30, 200), np.logspace(-30, 300, 200)]
    dataset = np.vstack((x + 0j, sc.digamma(x))).T
    FuncData(sc.digamma, dataset, 0, 1, rtol=5e-14, nan_ok=True).check()


def test_consistency():
    # Make sure the implementation of spence for real arguments
    # agrees with the implementation of spence for imaginary arguments.

    x = np.logspace(-30, 300, 200)
    dataset = np.vstack((x + 0j, spence(x))).T
    FuncData(spence, dataset, 0, 1, rtol=1e-14).check()


def test_consistency():
    # Check that our hash doesn't change because of a mistake
    # in the actual code; this is the ground truth.
    result = hash_pandas_object(Index(["foo", "bar", "baz"]))
    expected = Series(
        np.array(
            [3600424527151052760, 1374399572096150070, 477881037637427054],
            dtype="uint64",
        ),
        index=["foo", "bar", "baz"],
    )
    tm.assert_series_equal(result, expected)


def test_consistency():
    # need to construct an overflow
    major_axis = list(range(70000))
    minor_axis = list(range(10))

    major_codes = np.arange(70000)
    minor_codes = np.repeat(range(10), 7000)

    # the fact that is works means it's consistent
    index = MultiIndex(
        levels=[major_axis, minor_axis], codes=[major_codes, minor_codes]
    )

    # inconsistent
    major_codes = np.array([0, 0, 1, 1, 1, 2, 2, 3, 3])
    minor_codes = np.array([0, 1, 0, 1, 1, 0, 1, 0, 1])
    index = MultiIndex(
        levels=[major_axis, minor_axis], codes=[major_codes, minor_codes]
    )

    assert index.is_unique is False

