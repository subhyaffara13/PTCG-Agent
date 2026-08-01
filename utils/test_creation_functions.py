
def test_creation_functions():
    assert_array_equal(np.zeros(3, dtype="T"), ["", "", ""])
    assert_array_equal(np.empty(3, dtype="T"), ["", "", ""])

    assert np.zeros(3, dtype="T")[0] == ""
    assert np.empty(3, dtype="T")[0] == ""

