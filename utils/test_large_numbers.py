
def test_large_numbers():
    df = DataFrame({"A": [1e308, 2e308]})
    result = df.to_csv(float_format="{:.2e}", lineterminator="\n")
    expected = ",A\n0,1.00e+308\n1,inf\n"
    assert result == expected

