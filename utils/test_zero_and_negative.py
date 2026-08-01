
def test_zero_and_negative():
    df = DataFrame({"A": [0.0, -1.23456]})
    result = df.to_csv(float_format="{:+.2f}", lineterminator="\n")
    expected = ",A\n0,+0.00\n1,-1.23\n"
    assert result == expected

