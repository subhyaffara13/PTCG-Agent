
def test_as_euler_symmetric_axes(xp, seq_tuple, intrinsic):
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
    angles[:, 1] = rnd.uniform(low=0, high=np.pi, size=(n,))
    angles[:, 2] = rnd.uniform(low=-np.pi, high=np.pi, size=(n,))
    angles = xp.asarray(angles)

    # Rotation of the form A/B/A are rotation around symmetric axes
    seq = "".join([seq_tuple[0], seq_tuple[1], seq_tuple[0]])
    if intrinsic:
        seq = seq.upper()
    rotation = Rotation.from_euler(seq, angles)
    angles_quat = rotation.as_euler(seq)
    xp_assert_close(angles, angles_quat, atol=0, rtol=1.1e-13)
    test_stats(angles_quat - angles, 1e-16, 1e-14)

