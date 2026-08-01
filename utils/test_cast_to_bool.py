
def test_cast_to_bool(strings, cast_answer, any_answer, all_answer):
    sarr = np.array(strings, dtype="T")
    assert_array_equal(sarr.astype("bool"), cast_answer)

    assert np.any(sarr) == any_answer
    assert np.all(sarr) == all_answer

