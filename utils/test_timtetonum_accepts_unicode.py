
def test_timtetonum_accepts_unicode():
    assert converter.time2num("00:01") == converter.time2num("00:01")

