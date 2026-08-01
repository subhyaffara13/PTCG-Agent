
def test_join_invalid_validate(left_no_dup, right_no_dup):
    # GH 46622
    # Check invalid arguments
    msg = (
        '"invalid" is not a valid argument. '
        "Valid arguments are:\n"
        '- "1:1"\n'
        '- "1:m"\n'
        '- "m:1"\n'
        '- "m:m"\n'
        '- "one_to_one"\n'
        '- "one_to_many"\n'
        '- "many_to_one"\n'
        '- "many_to_many"'
    )
    with pytest.raises(ValueError, match=msg):
        left_no_dup.merge(right_no_dup, on="a", validate="invalid")

