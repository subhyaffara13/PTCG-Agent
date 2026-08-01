
def test_pickle_roundtrip_containers(as_frame, values, dtype, temp_file):
    s = pd.Series(pd.array(values, dtype=dtype))
    if as_frame:
        s = s.to_frame(name="A")
    result = tm.round_trip_pickle(s, temp_file)
    tm.assert_equal(result, s)

