
def test_new_style_with_template():
    df = DataFrame({"A": [1234.56789]})
    result = df.to_csv(float_format="Value: {:,.2f}", lineterminator="\n")
    expected = ',A\n0,"Value: 1,234.57"\n'
    assert result == expected

