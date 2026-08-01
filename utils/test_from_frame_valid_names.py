
def test_from_frame_valid_names(names_in, names_out):
    # GH 22420
    df = pd.DataFrame(
        [["a", "a"], ["a", "b"], ["b", "a"], ["b", "b"]],
        columns=MultiIndex.from_tuples([("L1", "x"), ("L2", "y")]),
    )
    mi = MultiIndex.from_frame(df, names=names_in)
    assert mi.names == names_out

