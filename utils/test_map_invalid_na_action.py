
def test_map_invalid_na_action(float_frame):
    # GH 23803
    with pytest.raises(ValueError, match="na_action must be .*Got 'abc'"):
        float_frame.map(lambda x: len(str(x)), na_action="abc")

