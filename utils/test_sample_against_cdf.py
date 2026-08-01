
def test_sample_against_cdf(family, dist_shape, x_shape, fname, rng_type):
    rng = np.random.default_rng(842582438235635)
    num_parameters = family._num_parameters()

    if dist_shape and num_parameters == 0:
        pytest.skip("Distribution can't have a shape without parameters.")

    dist = family._draw(dist_shape, rng)

    n = 1024
    sample_size = (n,) + x_shape
    sample_array_shape = sample_size + dist_shape

    if fname == 'sample':
        sample_method = dist.sample

    if rng_type != np.random.Generator:
        rng = rng_type(d=1, seed=rng)
    x = sample_method(sample_size, rng=rng)
    assert x.shape == sample_array_shape

    # probably should give `axis` argument to ks_1samp, review that separately
    statistic = _kolmogorov_smirnov(dist, x, axis=0)
    pvalue = kolmogn(x.shape[0], statistic, cdf=False)
    p_threshold = 0.01
    num_pvalues = pvalue.size
    num_small_pvalues = np.sum(pvalue < p_threshold)
    assert num_small_pvalues < p_threshold * num_pvalues

