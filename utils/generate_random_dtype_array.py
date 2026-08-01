
def generate_random_dtype_array(shape, dtype, rng):
    # generates a random matrix of desired data type of shape
    if dtype in COMPLEX_DTYPES:
        return (rng.rand(*shape)
                + rng.rand(*shape)*1.0j).astype(dtype)
    return rng.rand(*shape).astype(dtype)

