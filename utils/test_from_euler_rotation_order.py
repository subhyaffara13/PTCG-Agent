
def test_from_euler_rotation_order(xp):
    # Intrinsic rotation is same as extrinsic with order reversed
    rnd = np.random.RandomState(0)
    a = xp.asarray(rnd.randint(low=0, high=180, size=(6, 3)))
    b = xp.flip(a, axis=-1)
    x = Rotation.from_euler('xyz', a, degrees=True).as_quat()
    y = Rotation.from_euler('ZYX', b, degrees=True).as_quat()
    xp_assert_close(x, y)

