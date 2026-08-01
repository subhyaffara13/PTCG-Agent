
def test_frame_set_name_single(df):
    grouped = df.groupby("A")

    result = grouped.mean(numeric_only=True)
    assert result.index.name == "A"

    result = df.groupby("A", as_index=False).mean(numeric_only=True)
    assert result.index.name != "A"

    result = grouped[["C", "D"]].agg("mean")
    assert result.index.name == "A"

    result = grouped.agg({"C": "mean", "D": "std"})
    assert result.index.name == "A"

    result = grouped["C"].mean()
    assert result.index.name == "A"
    result = grouped["C"].agg("mean")
    assert result.index.name == "A"
    result = grouped["C"].agg(["mean", "std"])
    assert result.index.name == "A"

    msg = r"nested renamer is not supported"
    with pytest.raises(SpecificationError, match=msg):
        grouped["C"].agg({"foo": "mean", "bar": "std"})

