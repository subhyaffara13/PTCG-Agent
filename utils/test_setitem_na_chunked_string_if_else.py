
def test_setitem_na_chunked_string_if_else():
    # GH#64320
    df = pd.concat(
        [
            pd.DataFrame({"a": ["x"] * 5, "b": ["x"] * 5}),
            pd.DataFrame({"a": ["x"] * 5, "b": ["x"] * 5}),
        ],
        ignore_index=True,
    )
    for _ in range(5):
        df.loc[[0], "a"] = pd.NA
    assert pd.isna(df["a"].iloc[0])
    assert (df["a"].iloc[1:] == "x").all()
    assert (df["b"] == "x").all()

