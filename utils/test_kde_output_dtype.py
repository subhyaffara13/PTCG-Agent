
def test_kde_output_dtype(dtype, bw_type):
    # Check whether the datatypes are available
    dtype = getattr(np, dtype, None)

    if bw_type in ["scott", "silverman"]:
        bw = bw_type
    else:
        bw_type = getattr(np, bw_type, None)
        bw = bw_type(3) if bw_type else None

    if any(dt is None for dt in [dtype, bw]):
        pytest.skip()

    weights = np.arange(5, dtype=dtype)
    dataset = np.arange(5, dtype=dtype)
    k = stats.gaussian_kde(dataset, bw_method=bw, weights=weights)
    points = np.arange(5, dtype=dtype)
    result = k(points)
    # weights are always cast to float64
    assert result.dtype == np.result_type(dataset, points, np.float64(weights),
                                          k.factor)

