
def test_from_arrow_respecting_given_dtype():
    date_array = pa.array(
        [pd.Timestamp("2019-12-31"), pd.Timestamp("2019-12-31")], type=pa.date32()
    )
    result = date_array.to_pandas(
        types_mapper={pa.date32(): ArrowDtype(pa.date64())}.get
    )
    expected = pd.Series(
        [pd.Timestamp("2019-12-31"), pd.Timestamp("2019-12-31")],
        dtype=ArrowDtype(pa.date64()),
    )
    tm.assert_series_equal(result, expected)

