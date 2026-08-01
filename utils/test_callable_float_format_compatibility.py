
def test_callable_float_format_compatibility():
    df = DataFrame({"A": [1234.56789, 9876.54321]})
    result = df.to_csv(float_format=lambda x: f"{x:,.2f}", lineterminator="\n")
    expected = ',A\n0,"1,234.57"\n1,"9,876.54"\n'
    assert result == expected

