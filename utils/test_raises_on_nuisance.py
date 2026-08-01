
def test_raises_on_nuisance(df, using_infer_string):
    grouped = df.groupby("A")
    msg = re.escape("agg function failed [how->mean,dtype->")
    if using_infer_string:
        msg = "dtype 'str' does not support operation 'mean'"
    with pytest.raises(TypeError, match=msg):
        grouped.agg("mean")
    with pytest.raises(TypeError, match=msg):
        grouped.mean()

    df = df.loc[:, ["A", "C", "D"]]
    df["E"] = datetime.now()
    grouped = df.groupby("A")
    msg = "datetime64 type does not support operation 'sum'"
    with pytest.raises(TypeError, match=msg):
        grouped.agg("sum")
    with pytest.raises(TypeError, match=msg):
        grouped.sum()

