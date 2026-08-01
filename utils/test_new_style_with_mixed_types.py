
def test_new_style_with_mixed_types():
    df = DataFrame({"A": [1.23, 4.56], "B": ["x", "y"]})
    result = df.to_csv(float_format="{:.2f}", lineterminator="\n")
    expected = ",A,B\n0,1.23,x\n1,4.56,y\n"
    assert result == expected

