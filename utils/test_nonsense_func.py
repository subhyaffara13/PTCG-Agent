
def test_nonsense_func():
    df = DataFrame([0])
    msg = r"unsupported operand type\(s\) for \+: 'int' and 'str'"
    with pytest.raises(TypeError, match=msg):
        df.groupby(lambda x: x + "foo")

