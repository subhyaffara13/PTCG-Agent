
def test_string_without_numbers(value):
    # GH39710 Timedelta input string with only symbols and no digits raises an error
    msg = (
        "symbols w/o a number"
        if value != "--"
        else "only leading negative signs are allowed"
    )
    with pytest.raises(ValueError, match=msg):
        Timedelta(value)

