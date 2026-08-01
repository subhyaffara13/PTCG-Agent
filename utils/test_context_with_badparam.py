
def test_context_with_badparam():
    original_value = 'gray'
    other_value = 'blue'
    with style.context({PARAM: other_value}):
        assert mpl.rcParams[PARAM] == other_value
        x = style.context({PARAM: original_value, 'badparam': None})
        with pytest.raises(KeyError,
                           match=r"'badparam' is not a valid value for rcParam\."):
            with x:
                pass
        assert mpl.rcParams[PARAM] == other_value

