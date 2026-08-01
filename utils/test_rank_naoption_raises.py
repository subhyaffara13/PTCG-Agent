
def test_rank_naoption_raises(rank_method, ascending, na_option, pct, vals):
    df = DataFrame({"key": ["foo"] * 5, "val": vals})
    msg = "na_option must be one of 'keep', 'top', or 'bottom'"

    with pytest.raises(ValueError, match=msg):
        df.groupby("key").rank(
            method=rank_method, ascending=ascending, na_option=na_option, pct=pct
        )

