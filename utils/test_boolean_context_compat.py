
def test_boolean_context_compat(index):
    # GH#7897
    with pytest.raises(ValueError, match="The truth value of a"):
        if index:
            pass

    with pytest.raises(ValueError, match="The truth value of a"):
        bool(index)

