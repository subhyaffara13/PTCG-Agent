
def test_pickle_roundtrip_pandas(temp_file):
    result = tm.round_trip_pickle(NA, temp_file)
    assert result is NA

