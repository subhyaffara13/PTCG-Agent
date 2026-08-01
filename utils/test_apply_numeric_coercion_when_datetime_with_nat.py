
def test_apply_numeric_coercion_when_datetime_with_nat():
    # GH 14423
    def predictions(tool):
        out = Series(index=["p1", "p2", "useTime"], dtype=object)
        if "step1" in list(tool.State):
            out["p1"] = str(tool[tool.State == "step1"].Machine.values[0])
        if "step2" in list(tool.State):
            out["p2"] = str(tool[tool.State == "step2"].Machine.values[0])
            out["useTime"] = str(tool[tool.State == "step2"].oTime.values[0])
        return out

    df1 = DataFrame(
        {
            "Key": ["B", "B", "A", "A"],
            "State": ["step1", "step2", "step1", "step2"],
            "oTime": ["", "2016-09-19 05:24:33", "", "2016-09-19 23:59:04"],
            "Machine": ["23", "36L", "36R", "36R"],
        }
    )
    df2 = df1.copy()
    df2.oTime = pd.to_datetime(df2.oTime)
    expected = df1.groupby("Key").apply(predictions).p1
    result = df2.groupby("Key").apply(predictions).p1
    tm.assert_series_equal(expected, result)

