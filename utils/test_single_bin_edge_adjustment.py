
def test_single_bin_edge_adjustment(values, threshold):
    # gh-58517 - edge adjustment mutation when all values are same
    result, bins = cut(values, 3, retbins=True)

    bin_range = bins[-1] - bins[0]
    assert bin_range < threshold

