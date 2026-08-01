
def test_put_compression(temp_hdfstore):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )

    temp_hdfstore.put("c", df, format="table", complib="zlib")
    tm.assert_frame_equal(temp_hdfstore["c"], df)

    # can't compress if format='fixed'
    msg = "Compression not supported on Fixed format stores"
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.put("b", df, format="fixed", complib="zlib")

