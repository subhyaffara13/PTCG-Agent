
def test_abs_nan_signbit(dtype):
    """#31421 abs(nan) preserves positive sign bit correctly."""
    pos_nan = dtype(np.nan)
    assert not np.signbit(np.abs(pos_nan)), \
        f"abs(+nan) should have positive sign for {dtype.__name__}"

    neg_nan = dtype(-np.nan)
    assert not np.signbit(np.abs(neg_nan)), \
        f"abs(-nan) should have positive sign for {dtype.__name__}"

