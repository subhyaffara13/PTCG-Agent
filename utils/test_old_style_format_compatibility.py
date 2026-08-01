
def test_old_style_format_compatibility():
    df = DataFrame({"A": [1234.56789, 9876.54321]})
    result = df.to_csv(float_format="%.2f", lineterminator="\n")
    expected = ",A\n0,1234.57\n1,9876.54\n"
    assert result == expected

