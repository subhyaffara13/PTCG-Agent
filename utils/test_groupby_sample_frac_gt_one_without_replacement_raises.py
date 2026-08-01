
def test_groupby_sample_frac_gt_one_without_replacement_raises():
    df = DataFrame({"a": [1, 2], "b": [1, 2]})
    msg = "Replace has to be set to `True` when upsampling the population `frac` > 1."

    with pytest.raises(ValueError, match=msg):
        df.groupby("a").sample(frac=1.5, replace=False)

    with pytest.raises(ValueError, match=msg):
        df.groupby("a")["b"].sample(frac=1.5, replace=False)

