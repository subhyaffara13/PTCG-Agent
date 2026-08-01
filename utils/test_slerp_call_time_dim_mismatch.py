
def test_slerp_call_time_dim_mismatch(xp):
    rnd = np.random.RandomState(0)
    r = Rotation.from_quat(xp.asarray(rnd.uniform(size=(5, 4))))
    t = xp.arange(5)
    s = Slerp(t, r)

    with pytest.raises(ValueError,
                       match="`times` must be at most 1-dimensional."):
        interp_times = xp.asarray([[3.5],
                                   [4.2]])
        s(interp_times)

