
def test_approx_equal(xp):
    rng = np.random.default_rng(146972845698875399755764481408308808739)
    p = Rotation.random(10, rng=rng)
    q = Rotation.random(10, rng=rng)
    r_mag = (p * q.inv()).magnitude()
    p = rotation_to_xp(p, xp)
    q = rotation_to_xp(q, xp)
    # ensure we get mix of Trues and Falses
    atol = xp.asarray(np.median(r_mag))
    xp_assert_equal(p.approx_equal(q, atol), (xp.asarray(r_mag) < atol))

