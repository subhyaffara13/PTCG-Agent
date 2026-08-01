
def test_orc_dtype_backend_pyarrow(using_infer_string):
    pytest.importorskip("pyarrow")
    df = pd.DataFrame(
        {
            "string": list("abc"),
            "string_with_nan": ["a", np.nan, "c"],
            "string_with_none": ["a", None, "c"],
            "bytes": [b"foo", b"bar", None],
            "int": list(range(1, 4)),
            "float": np.arange(4.0, 7.0, dtype="float64"),
            "float_with_nan": [2.0, np.nan, 3.0],
            "bool": [True, False, True],
            "bool_with_na": [True, False, None],
            "datetime": pd.date_range("20130101", periods=3, unit="ns"),
            "datetime_with_nat": [
                pd.Timestamp("20130101"),
                pd.NaT,
                pd.Timestamp("20130103"),
            ],
        }
    )
    # FIXME: without casting to ns we do not round-trip correctly
    df["datetime_with_nat"] = df["datetime_with_nat"].astype("M8[ns]")

    bytes_data = df.copy().to_orc()
    result = read_orc(BytesIO(bytes_data), dtype_backend="pyarrow")

    expected = pd.DataFrame(
        {
            col: pd.arrays.ArrowExtensionArray(pa.array(df[col], from_pandas=True))
            for col in df.columns
        }
    )
    if using_infer_string:
        # ORC does not preserve distinction between string and large string
        # -> the default large string comes back as string
        string_dtype = pd.ArrowDtype(pa.string())
        expected["string"] = expected["string"].astype(string_dtype)
        expected["string_with_nan"] = expected["string_with_nan"].astype(string_dtype)
        expected["string_with_none"] = expected["string_with_none"].astype(string_dtype)

    tm.assert_frame_equal(result, expected)

