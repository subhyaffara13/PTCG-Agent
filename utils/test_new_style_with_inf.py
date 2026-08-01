
def test_new_style_with_inf():
    df = DataFrame({"A": [1.23, np.inf, -np.inf]})
    result = df.to_csv(float_format="{:.2f}", na_rep="NA", lineterminator="\n")
    expected = ",A\n0,1.23\n1,inf\n2,-inf\n"
    assert result == expected

