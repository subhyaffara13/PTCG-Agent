
def test_keys(d, Asp):
    assert Asp.keys() == d.keys()


def test_keys(temp_hdfstore):
    temp_hdfstore["a"] = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    temp_hdfstore["b"] = Series(
        range(10), dtype="float64", index=[f"i_{i}" for i in range(10)]
    )
    temp_hdfstore["c"] = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )

    assert len(temp_hdfstore) == 3
    expected = {"/a", "/b", "/c"}
    assert set(temp_hdfstore.keys()) == expected
    assert set(temp_hdfstore) == expected


def test_keys() -> None:
    """Test that ``TYPES.keys()`` and ``numpy.typing.__all__`` are synced."""
    keys = TYPES.keys()
    ref = set(npt.__all__)
    assert keys == ref

