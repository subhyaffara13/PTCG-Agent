
def test_serializable(obj, temp_file):
    # GH 35611
    unpickled = tm.round_trip_pickle(obj, temp_file)
    assert type(obj) == type(unpickled)

