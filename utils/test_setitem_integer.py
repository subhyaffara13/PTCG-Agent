
def test_setitem_integer(xp):
    rng = np.random.default_rng(146972845698875399755764481408308808739)
    r1 = rotation_to_xp(Rotation.random(10, rng=rng), xp)
    r2 = rotation_to_xp(Rotation.random(rng=rng), xp)
    r1[1] = r2
    xp_assert_equal(r1[1].as_quat(), r2.as_quat())

    # Multiple dimensions
    r1 = Rotation.from_quat(xp.asarray(rng.normal(size=(3, 5, 4))))
    r2 = Rotation.from_quat(xp.asarray(rng.normal(size=(5, 4))))
    r1[1] = r2
    xp_assert_equal(r1[1].as_quat(), r2.as_quat())

