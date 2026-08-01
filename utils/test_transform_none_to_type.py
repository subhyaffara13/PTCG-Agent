
def test_transform_none_to_type():
    # GH#34377
    df = DataFrame({"a": [None]})
    msg = "argument must be a"
    with pytest.raises(TypeError, match=msg):
        df.transform({"a": lambda x: int(x.iloc[0])})

