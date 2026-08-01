
def test_close_error_name():
    with pytest.raises(
        KeyError,
        match=(
            r"'grays' is not a valid value for colormap\. "
            r"Did you mean one of: 'gray', 'Grays', 'gray_r'\?")):
        matplotlib.colormaps["grays"]
    with pytest.raises(
        KeyError,
        match=(
            "'set' is not a valid value for sequence_name. "
            "Did you mean one of: 'Set3', 'Set2', 'Set1'?")):
        matplotlib.color_sequences["set"]

