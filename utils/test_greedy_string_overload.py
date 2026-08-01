
def test_greedy_string_overload():
    """Tests fix for #685 - ndarray shouldn't go to std::string overload"""

    assert m.issue685("abc") == "string"
    assert m.issue685(np.array([97, 98, 99], dtype="b")) == "array"
    assert m.issue685(123) == "other"

