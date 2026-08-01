
def test_mixed_arrays_and_python_scalars(xp):
    # Tests that the delegation infrastructure respects NEP50.
    res = special.fdtrc(1.1, 2., xp.asarray(1., dtype=xp.float32))
    ref = xp.asarray(0.4349004, dtype=xp.float32)
    xp_assert_close(res, ref)

