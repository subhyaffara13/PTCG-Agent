import math


def test_past_180_degree_rotation(xp):
    # ensure that a > 180 degree rotation is returned as a <180 rotation in MRPs
    # in this case 270 should be returned as -90
    expected_mrp = xp.asarray([-math.tan(xp.pi / 2 / 4), 0.0, 0])
    xp_assert_close(
        Rotation.from_euler('xyz', xp.asarray([270, 0, 0]), degrees=True).as_mrp(),
        expected_mrp,
    )

