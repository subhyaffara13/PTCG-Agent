
def test_size():
    x = Symbol('x', real=True)
    sx = size(x)
    assert fcode(sx, source_format='free') == 'size(x)'


def test_size(df, by):
    grouped = df.groupby(by=by)
    result = grouped.size()
    for key, group in grouped:
        assert result[key] == len(group)


def test_size(data, index, expected):
    # GH#52897
    df = DataFrame(data, index=index)
    assert df.size == expected
    assert isinstance(df.size, int)

