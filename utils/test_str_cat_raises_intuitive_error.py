
def test_str_cat_raises_intuitive_error(index_or_series):
    # GH 11334
    box = index_or_series
    s = box(["a", "b", "c", "d"])
    message = "Did you mean to supply a `sep` keyword?"
    with pytest.raises(ValueError, match=message):
        s.str.cat("|")
    with pytest.raises(ValueError, match=message):
        s.str.cat("    ")

