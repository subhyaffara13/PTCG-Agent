
def test_frame_mixed_numeric_object_with_timestamp(ts_value):
    # GH 13912
    df = DataFrame({"a": [1], "b": [1.1], "c": ["foo"], "d": [ts_value]})
    with pytest.raises(TypeError, match="does not support operation|Cannot perform"):
        df.sum()

