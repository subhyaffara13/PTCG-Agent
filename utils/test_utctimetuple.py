import time

def test_utctimetuple():
    # GH 32174
    ts = Timestamp("2000-01-01", tz="UTC")
    result = ts.utctimetuple()
    expected = time.struct_time((2000, 1, 1, 0, 0, 0, 5, 1, 0))
    assert result == expected

