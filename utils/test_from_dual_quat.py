
def test_from_dual_quat(xp, ndim: int):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-7
    shape = (ndim,) * (ndim - 1)

    # identity
    dq = xp.asarray([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0], dtype=dtype)
    dq = xp.tile(dq, shape + (1,))
    expected = xp.tile(xp.eye(4), shape + (1, 1))
    xp_assert_close(RigidTransform.from_dual_quat(dq).as_matrix(), expected, atol=atol)
    dq = xp.asarray([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=dtype)
    dq = xp.tile(dq, shape + (1,))
    xp_assert_close(RigidTransform.from_dual_quat(dq, scalar_first=True).as_matrix(),
                    expected, atol=atol)

    # only translation
    dq = xp.asarray([0, 0, 0, 1, 0.25, 0.15, -0.7, 0], dtype=dtype)
    dq = xp.tile(dq, shape + (1,))
    actual = RigidTransform.from_dual_quat(dq)
    expected_matrix = xp.asarray([
        [1, 0, 0, 0.5],
        [0, 1, 0, 0.3],
        [0, 0, 1, -1.4],
        [0, 0, 0, 1]
    ])
    expected_matrix = xp.tile(expected_matrix, shape + (1, 1))
    xp_assert_close(actual.as_matrix(), expected_matrix, atol=atol)
    dq = xp.asarray([1, 0, 0, 0, 0, 0.25, 0.15, -0.7], dtype=dtype)
    dq = xp.tile(dq, shape + (1,))
    actual = RigidTransform.from_dual_quat(dq, scalar_first=True)
    xp_assert_close(actual.as_matrix(), expected_matrix, atol=atol)

    # only rotation
    angles = xp.asarray([65, -13, 90], dtype=dtype)
    angles = xp.tile(angles, shape + (1,))
    actual_rot = Rotation.from_euler("xyz", angles, degrees=True)
    qrot = actual_rot.as_quat()
    dq = xp.concat((qrot, xp.zeros_like(qrot)), axis=-1)
    actual = RigidTransform.from_dual_quat(dq)
    expected_matrix = xp.tile(xp.eye(4), shape + (1, 1))
    expected_matrix = xpx.at(expected_matrix)[..., :3, :3].set(actual_rot.as_matrix())
    xp_assert_close(actual.as_matrix(), expected_matrix, atol=atol)

    qrot = actual_rot.as_quat(scalar_first=True)
    dq = xp.concat((qrot, xp.zeros_like(qrot)), axis=-1)
    actual = RigidTransform.from_dual_quat(dq, scalar_first=True)
    expected_matrix = xp.tile(xp.eye(4), shape + (1, 1))
    expected_matrix = xpx.at(expected_matrix)[..., :3, :3].set(actual_rot.as_matrix())
    xp_assert_close(actual.as_matrix(), expected_matrix, atol=atol)

    # rotation and translation
    # rtol is set to 1e-7 because xp_assert_close deviates from
    # np.testing.assert_allclose in that it does not automatically default to 1e-7 for
    # floating point inputs.
    # See https://numpy.org/doc/2.2/reference/generated/numpy.testing.assert_allclose.html
    dq = xp.asarray(
        [[0.0617101, -0.06483886, 0.31432811, 0.94508498,
          0.04985168, -0.26119618, 0.1691491, -0.07743254],
         [0.19507259, 0.49404931, -0.06091285, 0.8450749,
          0.65049656, -0.30782513, 0.16566752, 0.04174544]])
    dq = xp.tile(dq, shape + (1, 1))
    actual = RigidTransform.from_dual_quat(dq)
    expected_matrix = xp.asarray(
        [[[0.79398752, -0.60213598, -0.08376202, 0.24605262],
          [0.58613113, 0.79477941, -0.15740392, -0.4932833],
          [0.16135089, 0.07588122, 0.98397557, 0.34262676],
          [0., 0., 0., 1.]],
         [[0.50440981, 0.2957028, 0.81125249, 1.20934468],
          [0.08979911, 0.91647262, -0.3898898, -0.70540077],
          [-0.8587822, 0.26951399, 0.43572393, -0.47776265],
          [0., 0., 0., 1.]]])
    expected_matrix = xp.tile(expected_matrix, shape + (1, 1, 1))
    xp_assert_close(actual.as_matrix(), expected_matrix, atol=atol, rtol=1e-7)

    dq = xp.asarray(
        [[0.94508498, 0.0617101, -0.06483886, 0.31432811,
          -0.07743254, 0.04985168, -0.26119618, 0.1691491],
         [0.8450749, 0.19507259, 0.49404931, -0.06091285,
          0.04174544, 0.65049656, -0.30782513, 0.16566752]])
    dq = xp.tile(dq, shape + (1, 1))
    actual = RigidTransform.from_dual_quat(dq, scalar_first=True)
    xp_assert_close(actual.as_matrix(), expected_matrix, atol=atol, rtol=1e-7)

    # unnormalized dual quaternions

    # invalid real quaternion with norm 0
    dq = xp.zeros(shape + (8,))
    actual = RigidTransform.from_dual_quat(dq)
    expected = xp.tile(xp.eye(4), shape + (1, 1))
    xp_assert_close(actual.as_matrix(), expected, atol=atol)

    # real quaternion with norm != 1
    unnormalized_dual_quat = xp.asarray(
        [-0.2547655, 1.23506123, 0.20230088, 0.24247194,  # norm 1.3
         0.38559628, 0.08184063, 0.1755943, -0.1582222]  # orthogonal
    )
    xp_assert_close(xp_vector_norm(unnormalized_dual_quat[:4]), xp.asarray(1.3)[()],
                    atol=atol)
    xp_assert_close(xp.vecdot(unnormalized_dual_quat[:4],
                              unnormalized_dual_quat[4:])[()],
                    xp.asarray(0.0)[()], atol=1e-8)

    dq = xp.tile(unnormalized_dual_quat, shape + (1,))
    dual_quat = RigidTransform.from_dual_quat(dq).as_dual_quat()

    expected_ones = xp.ones(shape) if shape != () else xp.asarray(1.0)[()]
    expected_zeros = xp.zeros(shape) if shape != () else xp.asarray(0.0)[()]
    xp_assert_close(xp_vector_norm(dual_quat[..., :4], axis=-1), expected_ones,
                    atol=1e-12)
    vecdot = xp.vecdot(dual_quat[..., :4], dual_quat[..., 4:])
    vecdot = vecdot[()] if vecdot.shape == () else vecdot
    xp_assert_close(vecdot, expected_zeros, atol=atol)

    # real and dual quaternion are not orthogonal
    unnormalized_dual_quat = xp.asarray(
        [0.20824458, 0.75098079, 0.54542913, -0.30849493,  # unit norm
         -0.16051025, 0.10742978, 0.21277201, 0.20596935]  # not orthogonal
    )
    xp_assert_close(xp_vector_norm(unnormalized_dual_quat[:4]), xp.asarray(1.0)[()],
                    atol=atol)
    assert xp.vecdot(unnormalized_dual_quat[:4], unnormalized_dual_quat[4:]) != 0.0
    dq = xp.tile(unnormalized_dual_quat, shape + (1,))
    dual_quat = RigidTransform.from_dual_quat(dq).as_dual_quat()

    xp_assert_close(xp_vector_norm(dual_quat[..., :4], axis=-1), expected_ones,
                    atol=1e-12)
    vecdot = xp.vecdot(dual_quat[..., :4], dual_quat[..., 4:])
    vecdot = vecdot[()] if vecdot.shape == () else vecdot
    xp_assert_close(vecdot, expected_zeros, atol=atol)

    # invalid real quaternion with norm 0, non-orthogonal dual quaternion
    unnormalized_dual_quat = xp.asarray(
        [0.0, 0.0, 0.0, 0.0, -0.16051025, 0.10742978, 0.21277201, 0.20596935])
    assert xp.vecdot(xp.asarray([0.0, 0, 0, 1]), unnormalized_dual_quat[4:]) != 0.0
    dq = xp.tile(unnormalized_dual_quat, shape + (1,))
    dual_quat = RigidTransform.from_dual_quat(dq).as_dual_quat()

    xp_assert_close(xp_vector_norm(dual_quat[..., :4], axis=-1), expected_ones,
                    atol=1e-12)
    vecdot = xp.vecdot(dual_quat[..., :4], dual_quat[..., 4:])
    vecdot = vecdot[()] if vecdot.shape == () else vecdot
    xp_assert_close(vecdot, expected_zeros, atol=atol)

    # compensation for precision loss in real quaternion
    rng = np.random.default_rng(1000)
    t = xp.asarray(rng.normal(size=shape + (3,)), dtype=dtype)
    q = xp.asarray(rng.normal(size=shape + (4,)), dtype=dtype)
    r = Rotation.from_quat(q)
    random_dual_quats = RigidTransform.from_components(t, r).as_dual_quat()

    # ensure that random quaternions are not normalized
    random_dual_quats = xpx.at(random_dual_quats)[..., :4].add(0.01)
    assert not xp.any(xpx.isclose(xp_vector_norm(random_dual_quats[..., :4], axis=-1),
                                  1.0, atol=0.0001))
    dual_quat_norm = RigidTransform.from_dual_quat(
        random_dual_quats).as_dual_quat()
    xp_assert_close(xp_vector_norm(dual_quat_norm[..., :4], axis=-1), expected_ones,
                    atol=atol)

    # compensation for precision loss in dual quaternion, results in violation
    # of orthogonality constraint
    t = xp.asarray(rng.normal(size=shape + (3,)), dtype=dtype)
    q = xp.asarray(rng.normal(size=shape + (4,)), dtype=dtype)
    r = Rotation.from_quat(q)
    random_dual_quats = RigidTransform.from_components(t, r).as_dual_quat()

    # ensure that random quaternions are not normalized
    random_dual_quats = xpx.at(random_dual_quats)[..., 4:].add(0.1)
    q_norm = xp.vecdot(random_dual_quats[..., :4], random_dual_quats[..., 4:])
    assert not xp.any(xpx.isclose(q_norm, 0.0, atol=0.0001))
    dual_quat_norm = RigidTransform.from_dual_quat(
        random_dual_quats).as_dual_quat()
    vecdot = xp.vecdot(dual_quat[..., :4], dual_quat[..., 4:])
    vecdot = vecdot[()] if vecdot.shape == () else vecdot
    xp_assert_close(vecdot, expected_zeros, atol=atol)
    xp_assert_close(random_dual_quats[..., :4], dual_quat_norm[..., :4], atol=atol)

