
def test_branch_cut():
    # Make sure negative zero is treated correctly
    x = -np.logspace(300, -30, 100)
    z = np.asarray([complex(x0, 0.0) for x0 in x])
    zbar = np.asarray([complex(x0, -0.0) for x0 in x])
    assert_allclose(z, zbar.conjugate(), rtol=1e-15, atol=0)

