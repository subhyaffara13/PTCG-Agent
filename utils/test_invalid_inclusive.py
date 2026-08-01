
def test_invalid_inclusive(invalid_inclusive):
    with pytest.raises(
        ValueError,
        match="Inclusive has to be either 'both', 'neither', 'left' or 'right'",
    ):
        validate_inclusive(invalid_inclusive)

