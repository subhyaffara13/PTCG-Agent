
def test_tooltips_non_unique_raises(styler):
    # ttips has unique keys
    ttips = DataFrame([["1", "2"], ["3", "4"]], columns=["c", "d"], index=["a", "b"])
    styler.set_tooltips(ttips=ttips)  # OK

    # ttips has non-unique columns
    ttips = DataFrame([["1", "2"], ["3", "4"]], columns=["c", "c"], index=["a", "b"])
    with pytest.raises(KeyError, match="Tooltips render only if `ttips` has unique"):
        styler.set_tooltips(ttips=ttips)

    # ttips has non-unique index
    ttips = DataFrame([["1", "2"], ["3", "4"]], columns=["c", "d"], index=["a", "a"])
    with pytest.raises(KeyError, match="Tooltips render only if `ttips` has unique"):
        styler.set_tooltips(ttips=ttips)

