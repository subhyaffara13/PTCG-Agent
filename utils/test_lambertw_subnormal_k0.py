
def test_lambertw_subnormal_k0(z):
    # Verify that subnormal inputs are handled correctly on
    # the branch k=0 (regression test for gh-16291).
    w = lambertw(z)
    # For values this small, we can be sure that numerically,
    # lambertw(z) is z.
    assert w == z

