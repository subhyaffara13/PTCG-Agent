
def test_multi_column_float():
    df = DataFrame({"A": [1.23, 4.56], "B": [7.89, 0.12]})
    result = df.to_csv(float_format="{:.2f}", lineterminator="\n")
    expected = ",A,B\n0,1.23,7.89\n1,4.56,0.12\n"
    assert result == expected

