
def test_error_wrong_data_type():
    dummies = [0, 1, 0]
    with pytest.raises(
        TypeError,
        match=r"Expected 'data' to be a 'DataFrame'; Received 'data' of type: list",
    ):
        from_dummies(dummies)

