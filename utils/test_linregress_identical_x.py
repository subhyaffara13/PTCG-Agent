
def test_linregress_identical_x():
    rng = np.random.default_rng(74578245698)
    x = np.zeros(10)
    y = rng.random(10)
    msg = "Cannot calculate a linear regression if all x values are identical"
    with assert_raises(ValueError, match=msg):
        mstats.linregress(x, y)

