
def test_valid_inclusive(valid_inclusive, expected_tuple):
    resultant_tuple = validate_inclusive(valid_inclusive)
    assert expected_tuple == resultant_tuple

