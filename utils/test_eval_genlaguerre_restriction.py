
def test_eval_genlaguerre_restriction():
    # check it returns nan for alpha <= -1
    assert_(np.isnan(_ufuncs.eval_genlaguerre(0, -1, 0)))
    assert_(np.isnan(_ufuncs.eval_genlaguerre(0.1, -1, 0)))

