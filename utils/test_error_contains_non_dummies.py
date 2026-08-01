
def test_error_contains_non_dummies():
    dummies = DataFrame(
        {"a": [1, 6, 3, 1], "b": [0, 1, 0, 2], "c": ["c1", "c2", "c3", "c4"]}
    )
    with pytest.raises(
        TypeError,
        match=r"Passed DataFrame contains non-dummy data",
    ):
        from_dummies(dummies)

