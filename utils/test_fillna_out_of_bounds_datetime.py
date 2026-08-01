
def test_fillna_out_of_bounds_datetime():
    # GH#61208
    df = DataFrame(
        {
            "datetime": date_range("1/1/2011", periods=3, freq="h", unit="ns"),
            "value": [1, 2, 3],
        }
    )
    df.iloc[0, 0] = None

    msg = "Cannot cast 0001-01-01 00:00:00 to unit='ns' without overflow"
    with pytest.raises(OutOfBoundsDatetime, match=msg):
        df.fillna(Timestamp("0001-01-01"))

