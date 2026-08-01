
def test_nat_iso_format(get_nat):
    # see gh-12300
    assert get_nat("NaT").isoformat() == "NaT"
    assert get_nat("NaT").isoformat(timespec="nanoseconds") == "NaT"

