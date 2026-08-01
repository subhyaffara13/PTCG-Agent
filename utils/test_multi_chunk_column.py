
def test_multi_chunk_column() -> None:
    pytest.importorskip("pyarrow", "11.0.0")
    ser = pd.Series([1, 2, None], dtype="Int64[pyarrow]")
    df = pd.concat([ser, ser], ignore_index=True).to_frame("a")
    df_orig = df.copy()

    with tm.assert_produces_warning(match="Interchange"):
        with pytest.raises(
            RuntimeError,
            match="Found multi-chunk pyarrow array, but `allow_copy` is False",
        ):
            pd.api.interchange.from_dataframe(df.__dataframe__(allow_copy=False))
    with tm.assert_produces_warning(match="Interchange"):
        result = pd.api.interchange.from_dataframe(df.__dataframe__(allow_copy=True))
    # Interchange protocol defaults to creating numpy-backed columns, so currently this
    # is 'float64'.
    expected = pd.DataFrame({"a": [1.0, 2.0, None, 1.0, 2.0, None]}, dtype="float64")
    tm.assert_frame_equal(result, expected)

    # Check that the rechunking we did didn't modify the original DataFrame.
    tm.assert_frame_equal(df, df_orig)
    assert len(df["a"].array._pa_array.chunks) == 2
    assert len(df_orig["a"].array._pa_array.chunks) == 2

