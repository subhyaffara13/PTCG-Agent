
def test_no_float_format():
    df = DataFrame({"A": [1.23, 4.56]})
    result = df.to_csv(float_format=None, lineterminator="\n")
    expected = ",A\n0,1.23\n1,4.56\n"
    assert result == expected

