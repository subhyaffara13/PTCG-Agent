
def test_zoneinfo_fixed_offset(tz_name):
    # GH#64363
    zoneinfo = pytest.importorskip("zoneinfo")
    tz = zoneinfo.ZoneInfo(tz_name)
    assert timezones.is_fixed_offset(tz)

