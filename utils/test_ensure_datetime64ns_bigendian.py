
def test_ensure_datetime64ns_bigendian():
    # GH#29684
    arr = np.array([np.datetime64(1, "ms")], dtype=">M8[ms]")
    result = astype_overflowsafe(arr, dtype=np.dtype("M8[ns]"))

    expected = np.array([np.datetime64(1, "ms")], dtype="M8[ns]")
    tm.assert_numpy_array_equal(result, expected)

