
def test_localize_pydatetime_dt_types(dt, expected):
    # GH 25851
    # ensure that subclassed datetime works with
    # localize_pydatetime
    result = conversion.localize_pydatetime(dt, timezone.utc)
    assert result == expected

