
def test_context_with_dict_after_namedstyle():
    # Test dict after style name where dict modifies the same parameter.
    original_value = 'gray'
    other_value = 'blue'
    mpl.rcParams[PARAM] = original_value
    with temp_style('test', DUMMY_SETTINGS):
        with style.context(['test', {PARAM: other_value}]):
            assert mpl.rcParams[PARAM] == other_value
    assert mpl.rcParams[PARAM] == original_value

