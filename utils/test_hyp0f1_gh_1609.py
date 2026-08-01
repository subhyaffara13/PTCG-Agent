
def test_hyp0f1_gh_1609():
    # this is a regression test for gh-1609
    vv = np.linspace(150, 180, 21)
    af = sc.hyp0f1(vv, 0.5)
    mf = np.array([mpmath.hyp0f1(v, 0.5) for v in vv])
    assert_allclose(af, mf.astype(float), rtol=1e-12)

