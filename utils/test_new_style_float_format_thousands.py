
def test_new_style_float_format_thousands():
    df = DataFrame({"A": [1234.56789, 9876.54321]})
    result = df.to_csv(float_format="{:,.2f}", lineterminator="\n")
    expected = ',A\n0,"1,234.57"\n1,"9,876.54"\n'
    assert result == expected

