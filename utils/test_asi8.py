
def test_asi8():
    result = PeriodArray._from_sequence(["2000", "2001", None], dtype="period[D]").asi8
    expected = np.array([10957, 11323, iNaT])
    tm.assert_numpy_array_equal(result, expected)

