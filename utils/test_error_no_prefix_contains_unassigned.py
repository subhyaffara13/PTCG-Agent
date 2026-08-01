
def test_error_no_prefix_contains_unassigned():
    dummies = DataFrame({"a": [1, 0, 0], "b": [0, 1, 0]})
    with pytest.raises(
        ValueError,
        match=(
            r"Dummy DataFrame contains unassigned value\(s\); "
            r"First instance in row: 2"
        ),
    ):
        from_dummies(dummies)

