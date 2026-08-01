
def test_scalar_setitem_with_nested_value(value):
    # For numeric data, we try to unpack and thus raise for mismatching length
    df = DataFrame({"A": [1, 2, 3]})
    msg = "|".join(
        [
            "Must have equal len keys and value",
            "setting an array element with a sequence",
        ]
    )
    with pytest.raises(ValueError, match=msg):
        df.loc[0, "B"] = value

    # TODO For object dtype this happens as well, but should we rather preserve
    # the nested data and set as such?
    df = DataFrame({"A": [1, 2, 3], "B": np.array([1, "a", "b"], dtype=object)})
    with pytest.raises(ValueError, match="Must have equal len keys and value"):
        df.loc[0, "B"] = value

