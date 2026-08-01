
def test_zoneinfo_not_fixed_offset_with_historical_transition():
    # GH#64363
    zoneinfo = pytest.importorskip("zoneinfo")
    tz = zoneinfo.ZoneInfo("Africa/Lusaka")
    assert not timezones.is_fixed_offset(tz)

