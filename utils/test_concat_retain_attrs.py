
def test_concat_retain_attrs(data):
    # GH#41828
    df1 = data.copy()
    df1.attrs = {1: 1}
    df2 = data.copy()
    df2.attrs = {1: 1}
    df = concat([df1, df2])
    assert df.attrs[1] == 1

