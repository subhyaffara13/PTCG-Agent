
def test_concatenate(xp):
    atol = 1e-12

    # Test concatenation of transforms
    t1 = xp.asarray([1, 0, 0])
    r1 = Rotation.from_euler('z', xp.asarray(90), degrees=True)
    tf1 = RigidTransform.from_components(t1, r1)

    t2 = xp.asarray([0, 1, 0])
    r2 = Rotation.from_euler('x', xp.asarray(90), degrees=True)
    tf2 = RigidTransform.from_components(t2, r2)

    # Concatenate single transforms
    concatenated1 = RigidTransform.concatenate([tf1, tf2])
    xp_assert_close(concatenated1[0].as_matrix(), tf1.as_matrix(), atol=atol)
    xp_assert_close(concatenated1[1].as_matrix(), tf2.as_matrix(), atol=atol)

    # Concatenate multiple transforms
    concatenated2 = RigidTransform.concatenate([tf1, concatenated1])
    xp_assert_close(concatenated2[0].as_matrix(), tf1.as_matrix(), atol=atol)
    xp_assert_close(concatenated2[1].as_matrix(), tf1.as_matrix(), atol=atol)
    xp_assert_close(concatenated2[2].as_matrix(), tf2.as_matrix(), atol=atol)

    # Test ND concatenation
    tf3 = RigidTransform.from_translation(xp.reshape(xp.arange(18), (3, 2, 3)))
    tf4 = RigidTransform.from_translation(xp.reshape(xp.arange(18) + 18, (3, 2, 3)))
    concatenated3 = RigidTransform.concatenate([tf3, tf4])
    xp_assert_close(concatenated3.as_matrix()[:3, ...], tf3.as_matrix(), atol=atol)
    xp_assert_close(concatenated3.as_matrix()[3:, ...], tf4.as_matrix(), atol=atol)


def test_concatenate(xp):
    rotation = rotation_to_xp(Rotation.random(10, rng=0), xp)
    sizes = [1, 2, 3, 1, 3]
    starts = [0] + list(np.cumsum(sizes))
    split = [rotation[i:i + n] for i, n in zip(starts, sizes)]
    result = Rotation.concatenate(split)
    xp_assert_equal(rotation.as_quat(), result.as_quat())

    # Test Rotation input for multiple rotations
    result = Rotation.concatenate(rotation)
    xp_assert_equal(rotation.as_quat(), result.as_quat())

    # Test that a copy is returned
    assert rotation is not result

    # Test Rotation input for single rotations
    rng = np.random.default_rng(0)
    quat = xp.asarray(rng.normal(size=(5, 2, 4)))
    rotation = Rotation.from_quat(quat)
    r1 = Rotation.from_quat(quat[:3, ...])
    r2 = Rotation.from_quat(quat[3:, ...])
    result = Rotation.concatenate([r1, r2])
    xp_assert_equal(rotation.as_quat(), result.as_quat())


def test_concatenate(string_list):
    sarr = np.array(string_list, dtype="T")
    sarr_cat = np.array(string_list + string_list, dtype="T")

    assert_array_equal(np.concatenate([sarr], axis=0), sarr)

