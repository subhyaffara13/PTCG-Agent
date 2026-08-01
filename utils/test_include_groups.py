
def test_include_groups():
    # GH#7155
    df = DataFrame({"a": [1, 1, 2], "b": [3, 4, 5]})
    gb = df.groupby("a")
    with pytest.raises(ValueError, match="include_groups=True is no longer allowed"):
        gb.apply(lambda x: x.sum(), include_groups=True)

