
def test_slerp_num_rotations_mismatch(xp):
    with pytest.raises(ValueError, match="number of rotations to be equal to "
                                         "number of timestamps"):
        rnd = np.random.RandomState(0)
        r = Rotation.from_quat(xp.asarray(rnd.uniform(size=(5, 4))))
        t = xp.arange(7)
        Slerp(t, r)

