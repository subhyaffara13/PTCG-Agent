
def test_groupby_empty_list_raises():
    # GH 5289
    values = zip(range(10), range(10), strict=True)
    df = DataFrame(values, columns=["apple", "b"])
    msg = "Grouper and axis must be same length"
    with pytest.raises(ValueError, match=msg):
        df.groupby([[]])

