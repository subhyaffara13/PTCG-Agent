
def test_slerp_time_dim_mismatch(xp):
    with pytest.raises(ValueError,
                       match="times to be specified in a 1 dimensional array"):
        rnd = np.random.RandomState(0)
        r = Rotation.from_quat(xp.asarray(rnd.uniform(size=(2, 4))))
        t = xp.asarray([[1],
                        [2]])
        Slerp(t, r)

