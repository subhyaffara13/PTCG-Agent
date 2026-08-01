
def test_may_share_memory_manual():
    # Manual test cases for may_share_memory

    # Base arrays
    xs0 = [
        np.zeros([13, 21, 23, 22], dtype=np.int8),
        np.zeros([13, 21, 23 * 2, 22], dtype=np.int8)[:, :, ::2, :]
    ]

    # Generate all negative stride combinations
    xs = []
    for x in xs0:
        for ss in itertools.product(*(([slice(None), slice(None, None, -1)],) * 4)):
            xp = x[ss]
            xs.append(xp)

    for x in xs:
        # The default is a simple extent check
        assert_(np.may_share_memory(x[:, 0, :], x[:, 1, :]))
        assert_(np.may_share_memory(x[:, 0, :], x[:, 1, :], max_work=None))

        # Exact checks
        check_may_share_memory_exact(x[:, 0, :], x[:, 1, :])
        check_may_share_memory_exact(x[:, ::7], x[:, 3::3])

        try:
            xp = x.ravel()
            if xp.flags.owndata:
                continue
            xp = xp.view(np.int16)
        except ValueError:
            continue

        # 0-size arrays cannot overlap
        check_may_share_memory_exact(x.ravel()[6:6],
                                     xp.reshape(13, 21, 23, 11)[:, ::7])

        # Test itemsize is dealt with
        check_may_share_memory_exact(x[:, ::7],
                                     xp.reshape(13, 21, 23, 11))
        check_may_share_memory_exact(x[:, ::7],
                                     xp.reshape(13, 21, 23, 11)[:, 3::3])
        check_may_share_memory_exact(x.ravel()[6:7],
                                     xp.reshape(13, 21, 23, 11)[:, ::7])

    # Check unit size
    x = np.zeros([1], dtype=np.int8)
    check_may_share_memory_exact(x, x)
    check_may_share_memory_exact(x, x.copy())

