
def test_new_style_with_nan():
    df = DataFrame({"A": [1.23, np.nan, 4.56]})
    result = df.to_csv(float_format="{:.2f}", na_rep="NA", lineterminator="\n")
    expected = ",A\n0,1.23\n1,NA\n2,4.56\n"
    assert result == expected

