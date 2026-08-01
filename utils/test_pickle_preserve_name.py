
def test_pickle_preserve_name(name, temp_file):
    unpickled = tm.round_trip_pickle(
        Series(np.arange(10, dtype=np.float64), name=name), temp_file
    )
    assert unpickled.name == name

