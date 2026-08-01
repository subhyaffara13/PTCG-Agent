
def _sprandn_array(m, n, density=0.01, format="coo", dtype=None, rng=None):
    # Helper function for testing.
    rng = np.random.default_rng(rng)
    data_sampler = rng.standard_normal
    return construct.random_array((m, n), density=density, format=format, dtype=dtype,
                                  rng=rng, data_sampler=data_sampler)

