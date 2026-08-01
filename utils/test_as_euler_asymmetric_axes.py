
def test_as_euler_asymmetric_axes(xp, seq_tuple, intrinsic):
    # helper function for mean error tests
    def test_stats(error, mean_max, rms_max):
        mean = xp.mean(error, axis=0)
        std = xp.std(error, axis=0)
        rms = xp.hypot(mean, std)
        assert xp.all(xp.abs(mean) < mean_max)
        assert xp.all(rms < rms_max)

    rnd = np.random.RandomState(0)
    n = 1000
    angles = np.empty((n, 3))
    angles[:, 0] = rnd.uniform(low=-np.pi, high=np.pi, size=(n,))
    angles[:, 1] = rnd.uniform(low=-np.pi / 2, high=np.pi / 2, size=(n,))
    angles[:, 2] = rnd.uniform(low=-np.pi, high=np.pi, size=(n,))
    angles = xp.asarray(angles)

    seq = "".join(seq_tuple)
    if intrinsic:
        # Extrinsic rotation (w.r.t. global world) at lower case
        # intrinsic (WRT the object itself) lower case.
        seq = seq.upper()
    rotation = Rotation.from_euler(seq, angles)
    angles_quat = rotation.as_euler(seq)
    xp_assert_close(angles, angles_quat, atol=0, rtol=1e-12)
    test_stats(angles_quat - angles, 1e-15, 1e-14)

