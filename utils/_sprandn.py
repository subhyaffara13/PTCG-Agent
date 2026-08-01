
def _sprandn(m, n, density=0.01, format="coo", dtype=None, rng=None):
    # Helper function for testing.
    rng = np.random.default_rng(rng)
    data_rvs = rng.standard_normal
    return construct.random(m, n, density, format, dtype, rng, data_rvs)

