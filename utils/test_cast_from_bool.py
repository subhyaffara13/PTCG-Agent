
def test_cast_from_bool(strings, cast_answer):
    barr = np.array(strings, dtype=bool)
    assert_array_equal(barr.astype("T"), np.array(cast_answer, dtype="T"))

