
def test_no_default_pickle(temp_file):
    # GH#40397
    obj = tm.round_trip_pickle(lib.no_default, temp_file)
    assert obj is lib.no_default

