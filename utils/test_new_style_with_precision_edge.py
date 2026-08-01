
def test_new_style_with_precision_edge():
    df = DataFrame({"A": [1.23456789]})
    result = df.to_csv(float_format="{:.10f}", lineterminator="\n")
    expected = ",A\n0,1.2345678900\n"
    assert result == expected

