
def test_error_with_prefix_contains_unassigned(dummies_with_unassigned):
    with pytest.raises(
        ValueError,
        match=(
            r"Dummy DataFrame contains unassigned value\(s\); "
            r"First instance in row: 2"
        ),
    ):
        from_dummies(dummies_with_unassigned, sep="_")

