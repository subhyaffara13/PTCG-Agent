
def test_detect_chained_assignment():
    # Inplace ops, originally from:
    # https://stackoverflow.com/questions/20508968/series-fillna-in-a-multiindex-dataframe-does-not-fill-is-this-a-bug
    a = [12, 23]
    b = [123, None]
    c = [1234, 2345]
    d = [12345, 23456]
    tuples = [("eyes", "left"), ("eyes", "right"), ("ears", "left"), ("ears", "right")]
    events = {
        ("eyes", "left"): a,
        ("eyes", "right"): b,
        ("ears", "left"): c,
        ("ears", "right"): d,
    }
    multiind = MultiIndex.from_tuples(tuples, names=["part", "side"])
    zed = DataFrame(events, index=["a", "b"], columns=multiind)

    with tm.raises_chained_assignment_error():
        zed["eyes"]["right"].fillna(value=555, inplace=True)

