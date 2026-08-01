
def test_round_trip_float():
    arr = np.zeros((), np.float64)
    arr[()] = 37.2
    assert m.round_trip_float(arr) == 37.2

