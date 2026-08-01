
def df_full():
    return pd.DataFrame(
        {
            "string": list("abc"),
            "string_with_nan": ["a", np.nan, "c"],
            "string_with_none": ["a", None, "c"],
            "bytes": [b"foo", b"bar", b"baz"],
            "unicode": ["foo", "bar", "baz"],
            "int": list(range(1, 4)),
            "uint": np.arange(3, 6).astype("u1"),
            "float": np.arange(4.0, 7.0, dtype="float64"),
            "float_with_nan": [2.0, np.nan, 3.0],
            "bool": [True, False, True],
            "datetime": pd.date_range("20130101", periods=3, unit="ns"),
            "datetime_with_nat": [
                pd.Timestamp("20130101"),
                pd.NaT,
                pd.Timestamp("20130103"),
            ],
        }
    )

