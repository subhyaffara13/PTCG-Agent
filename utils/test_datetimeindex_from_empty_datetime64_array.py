
def test_datetimeindex_from_empty_datetime64_array(unit):
    idx = DatetimeIndex(np.array([], dtype=f"datetime64[{unit}]"))
    assert len(idx) == 0

