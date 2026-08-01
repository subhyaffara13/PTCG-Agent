
def test_zoneinfo_utc_to_local_pre_first_transition(key):
    # GH#64363 - verify that ZoneInfo offsets before the first historical
    # transition (LMT era) match what ZoneInfo itself returns. The "before"
    # offset must be utcoff[0] from the TZ data (matching CPython's C
    # implementation), NOT the first non-DST transition offset.
    tz = zoneinfo.ZoneInfo(key)
    ts = Timestamp("1850-01-01", tz="UTC").tz_convert(tz)

    expected = datetime(1850, 1, 1, tzinfo=timezone.utc).astimezone(tz)
    assert ts.minute == expected.minute

