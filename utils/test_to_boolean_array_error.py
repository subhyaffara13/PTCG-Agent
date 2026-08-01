
def test_to_boolean_array_error(values):
    # error in converting existing arrays to BooleanArray
    msg = "Need to pass bool-like value"
    with pytest.raises(TypeError, match=msg):
        pd.array(values, dtype="boolean")

