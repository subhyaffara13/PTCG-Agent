
def test_from_generic_mrp(xp):
    mrp = xp.asarray([
        [1, 2, 2],
        [1, -1, 0.5],
        [0, 0, 0]])
    expected_quat = xp.asarray([
        [0.2, 0.4, 0.4, -0.8],
        [0.61538462, -0.61538462, 0.30769231, -0.38461538],
        [0, 0, 0, 1]])
    xp_assert_close(Rotation.from_mrp(mrp).as_quat(), expected_quat)

