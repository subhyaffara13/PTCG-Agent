
def test_agg_no_column(cases, agg):
    msg = r"Label\(s\) \['result1', 'result2'\] do not exist"
    with pytest.raises(KeyError, match=msg):
        cases[["A", "B"]].agg(**agg)

