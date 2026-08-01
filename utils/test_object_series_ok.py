
def test_object_series_ok():
    class Dummy:
        def __init__(self, value) -> None:
            self.value = value

        def __add__(self, other):
            return self.value + other.value

    arr = np.array([Dummy(0), Dummy(1)])
    ser = pd.Series(arr)
    tm.assert_series_equal(np.add(ser, ser), pd.Series(np.add(ser, arr)))
    tm.assert_series_equal(np.add(ser, Dummy(1)), pd.Series(np.add(ser, Dummy(1))))

