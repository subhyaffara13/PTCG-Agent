
def test_to_boolean_array_from_strings_invalid_string():
    with pytest.raises(ValueError, match="cannot be cast"):
        BooleanArray._from_sequence_of_strings(["donkey"], dtype=pd.BooleanDtype())

