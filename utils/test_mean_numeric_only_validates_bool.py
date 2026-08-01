
def test_mean_numeric_only_validates_bool():
    # GH#62778

    df = DataFrame({"A": range(5), "B": range(5)})

    msg = "numeric_only accepts only Boolean values"
    with pytest.raises(ValueError, match=msg):
        df.groupby(["A"]).mean(["B"])

    with pytest.raises(ValueError, match=msg):
        df.groupby(["A"]).mean(numeric_only="True")

    with pytest.raises(ValueError, match=msg):
        df.groupby(["A"]).mean(numeric_only=1)

