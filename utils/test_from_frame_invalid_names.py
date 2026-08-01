
def test_from_frame_invalid_names(names, expected_error_msg):
    # GH 22420
    df = pd.DataFrame(
        [["a", "a"], ["a", "b"], ["b", "a"], ["b", "b"]],
        columns=MultiIndex.from_tuples([("L1", "x"), ("L2", "y")]),
    )
    with pytest.raises(ValueError, match=expected_error_msg):
        MultiIndex.from_frame(df, names=names)

