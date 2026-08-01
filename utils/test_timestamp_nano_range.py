
def test_timestamp_nano_range(nano):
    # GH 48255
    with pytest.raises(ValueError, match="nanosecond must be in 0..999"):
        Timestamp(year=2022, month=1, day=1, nanosecond=nano)

