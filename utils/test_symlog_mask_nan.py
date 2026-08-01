
def test_symlog_mask_nan():
    # Use a transform round-trip to verify that the forward and inverse
    # transforms work, and that they respect nans and/or masking.
    slt = SymmetricalLogTransform(10, 2, 1)
    slti = slt.inverted()

    x = np.arange(-1.5, 5, 0.5)
    out = slti.transform_non_affine(slt.transform_non_affine(x))
    assert_allclose(out, x)
    assert type(out) is type(x)

    x[4] = np.nan
    out = slti.transform_non_affine(slt.transform_non_affine(x))
    assert_allclose(out, x)
    assert type(out) is type(x)

    x = np.ma.array(x)
    out = slti.transform_non_affine(slt.transform_non_affine(x))
    assert_allclose(out, x)
    assert type(out) is type(x)

    x[3] = np.ma.masked
    out = slti.transform_non_affine(slt.transform_non_affine(x))
    assert_allclose(out, x)
    assert type(out) is type(x)

