
def test_transform_nuisance_raises(df, using_infer_string):
    # case that goes through _transform_item_by_item

    df.columns = ["A", "B", "B", "D"]

    # this also tests orderings in transform between
    # series/frame to make sure it's consistent
    grouped = df.groupby("A")

    gbc = grouped["B"]
    msg = "Could not convert"
    if using_infer_string:
        msg = "Cannot perform reduction 'mean' with string dtype"
    with pytest.raises(TypeError, match=msg):
        gbc.transform(lambda x: np.mean(x))

    with pytest.raises(TypeError, match=msg):
        df.groupby("A").transform(lambda x: np.mean(x))

