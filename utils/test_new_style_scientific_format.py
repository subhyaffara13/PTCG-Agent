
def test_new_style_scientific_format():
    df = DataFrame({"A": [0.000123, 0.000456]})
    result = df.to_csv(float_format="{:.2e}", lineterminator="\n")
    expected = ",A\n0,1.23e-04\n1,4.56e-04\n"
    assert result == expected

