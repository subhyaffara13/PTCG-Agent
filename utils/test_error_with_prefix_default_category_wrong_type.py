
def test_error_with_prefix_default_category_wrong_type(dummies_with_unassigned):
    with pytest.raises(
        TypeError,
        match=(
            r"Expected 'default_category' to be of type 'None', 'Hashable', or 'dict'; "
            r"Received 'default_category' of type: list"
        ),
    ):
        from_dummies(dummies_with_unassigned, sep="_", default_category=["x", "y"])

