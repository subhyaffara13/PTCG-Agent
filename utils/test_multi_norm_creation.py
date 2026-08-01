
def test_multi_norm_creation():
    # tests for mcolors.MultiNorm

    # test wrong input
    with pytest.raises(ValueError,
                       match="MultiNorm must be assigned an iterable"):
        mcolors.MultiNorm("linear")
    with pytest.raises(ValueError,
                       match="MultiNorm must be assigned at least one"):
        mcolors.MultiNorm([])
    with pytest.raises(ValueError,
                       match="MultiNorm must be assigned an iterable"):
        mcolors.MultiNorm(None)
    with pytest.raises(ValueError,
                       match="not a valid"):
        mcolors.MultiNorm(["linear", "bad_norm_name"])
    with pytest.raises(ValueError,
                       match="Each norm assigned to MultiNorm"):
        mcolors.MultiNorm(["linear", object()])

    norm = mpl.colors.MultiNorm(['linear', 'linear'])

