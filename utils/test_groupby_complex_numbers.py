
def test_groupby_complex_numbers():
    # GH 17927
    df = DataFrame(
        [
            {"a": 1, "b": 1 + 1j},
            {"a": 1, "b": 1 + 2j},
            {"a": 4, "b": 1},
        ]
    )
    expected = DataFrame(
        np.array([1, 1, 1], dtype=np.int64),
        index=Index([(1 + 1j), (1 + 2j), (1 + 0j)], name="b"),
        columns=Index(["a"]),
    )
    result = df.groupby("b", sort=False).count()
    tm.assert_frame_equal(result, expected)

    # Sorted by the magnitude of the complex numbers
    expected.index = Index([(1 + 0j), (1 + 1j), (1 + 2j)], name="b")
    result = df.groupby("b", sort=True).count()
    tm.assert_frame_equal(result, expected)

