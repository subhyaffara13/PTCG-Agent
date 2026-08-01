
def test_map_arg_is_dict_with_invalid_na_action_raises(input_na_action):
    # https://github.com/pandas-dev/pandas/issues/46588
    s = Series([1, 2, 3])
    msg = f"na_action must either be 'ignore' or None, {input_na_action} was passed"
    with pytest.raises(ValueError, match=msg):
        s.map({1: 2}, na_action=input_na_action)

