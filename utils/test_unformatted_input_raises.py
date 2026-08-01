
def test_unformatted_input_raises():
    valid, invalid = "2024-01-01", "N"
    ser = Series([valid] * start_caching_at + [invalid])
    msg = 'time data "N" doesn\'t match format "%Y-%m-%d"'

    with pytest.raises(ValueError, match=msg):
        to_datetime(ser, format="%Y-%m-%d", exact=True, cache=True)

