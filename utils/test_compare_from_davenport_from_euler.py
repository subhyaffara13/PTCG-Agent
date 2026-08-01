
def test_compare_from_davenport_from_euler(xp):
    dtype = xpx.default_dtype(xp)
    rnd = np.random.RandomState(0)
    n = 100
    angles = np.empty((n, 3))

    # symmetric sequences
    rtol = 1e-12 if dtype == xp.float64 else 1e-5
    angles[:, 0] = rnd.uniform(low=-np.pi, high=np.pi, size=(n,))
    angles[:, 1] = rnd.uniform(low=0, high=np.pi, size=(n,))
    angles[:, 2] = rnd.uniform(low=-np.pi, high=np.pi, size=(n,))
    angles = xp.asarray(angles, dtype=dtype)
    for order in ['extrinsic', 'intrinsic']:
        for seq_tuple in permutations('xyz'):
            seq = ''.join([seq_tuple[0], seq_tuple[1], seq_tuple[0]])
            ax = xp.asarray([basis_vec(i) for i in seq], dtype=dtype)
            if order == 'intrinsic':
                seq = seq.upper()
            eul = Rotation.from_euler(seq, angles)
            dav = Rotation.from_davenport(ax, order, angles)
            xp_assert_close(eul.as_quat(canonical=True), dav.as_quat(canonical=True),
                            rtol=rtol)

    # asymmetric sequences
    angles = xpx.at(angles)[:, 1].subtract(np.pi / 2)
    for order in ['extrinsic', 'intrinsic']:
        for seq_tuple in permutations('xyz'):
            seq = ''.join(seq_tuple)
            ax = xp.asarray([basis_vec(i) for i in seq], dtype=dtype)
            if order == 'intrinsic':
                seq = seq.upper()
            eul = Rotation.from_euler(seq, angles)
            dav = Rotation.from_davenport(ax, order, angles)
            xp_assert_close(eul.as_quat(), dav.as_quat(), rtol=rtol)

