
def test_error_with_prefix_sep_wrong_type(dummies_basic):
    with pytest.raises(
        TypeError,
        match=(
            r"Expected 'sep' to be of type 'str' or 'None'; "
            r"Received 'sep' of type: list"
        ),
    ):
        from_dummies(dummies_basic, sep=["_"])

