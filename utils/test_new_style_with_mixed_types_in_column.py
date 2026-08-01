
def test_new_style_with_mixed_types_in_column():
    df = DataFrame({"A": [1.23, "text", 4.56]})
    result = df.to_csv(float_format="{:.2f}", lineterminator="\n")
    expected = ",A\n0,1.23\n1,text\n2,4.56\n"
    assert result == expected

