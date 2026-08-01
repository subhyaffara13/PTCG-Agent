
def test_agg_none_to_type():
    # GH 40543
    df = DataFrame({"a": [None]})
    msg = re.escape("int() argument must be a string")
    with pytest.raises(TypeError, match=msg):
        df.agg({"a": lambda x: int(x.iloc[0])})

