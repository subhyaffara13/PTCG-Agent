
def test_from_frame_error(non_frame):
    # GH 22420
    with pytest.raises(TypeError, match="Input must be a DataFrame"):
        MultiIndex.from_frame(non_frame)

