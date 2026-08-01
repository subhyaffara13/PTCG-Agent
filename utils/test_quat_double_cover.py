
def test_quat_double_cover(xp):
    # See the Rotation.from_quat() docstring for scope of the quaternion
    # double cover property.
    # Check from_quat and as_quat(canonical=False)
    q = xp.asarray([0.0, 0, 0, -1])
    r = Rotation.from_quat(q)
    xp_assert_equal(q, r.as_quat(canonical=False))
    # Check composition and inverse
    q = xp.asarray([1.0, 0, 0, 1])/math.sqrt(2)  # 90 deg rotation about x
    r = Rotation.from_quat(q)
    r3 = r*r*r
    xp_assert_close(r.as_quat(canonical=False)*math.sqrt(2),
                    xp.asarray([1.0, 0, 0, 1]))
    xp_assert_close(r.inv().as_quat(canonical=False)*math.sqrt(2),
                    xp.asarray([-1.0, 0, 0, 1]))
    xp_assert_close(r3.as_quat(canonical=False)*math.sqrt(2),
                    xp.asarray([1.0, 0, 0, -1]))
    xp_assert_close(r3.inv().as_quat(canonical=False)*math.sqrt(2),
                    xp.asarray([-1.0, 0, 0, -1]))

    # More sanity checks
    xp_assert_close((r*r.inv()).as_quat(canonical=False),
                    xp.asarray([0.0, 0, 0, 1]), atol=2e-16)
    xp_assert_close((r3*r3.inv()).as_quat(canonical=False),
                    xp.asarray([0.0, 0, 0, 1]), atol=2e-16)
    xp_assert_close((r*r3).as_quat(canonical=False),
                    xp.asarray([0.0, 0, 0, -1]), atol=2e-16)
    xp_assert_close((r.inv() * r3.inv()).as_quat(canonical=False),
                    xp.asarray([0.0, 0, 0, -1]), atol=2e-16)

