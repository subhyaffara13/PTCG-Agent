
def test_apply_matrix_equivalence():
    """Test documented equivalence for single transform:
    `apply(vector) == translation + vector @ rotation.as_matrix().T.`"""
    t = np.array([1.0, 2.0, 3.0])
    r = Rotation.from_rotvec([0, 0, 1])
    tf = RigidTransform.from_components(t, r)
    # Single vector (3,)
    v = np.array([1.0, 0.0, 0.0])
    xp_assert_close(tf.apply(v), t + v @ r.as_matrix().T)
    # Multiple vectors (P, 3)
    arr = np.array([[1, 0, 0], [0, 1, 0]], dtype=float)
    xp_assert_close(tf.apply(arr), t + arr @ r.as_matrix().T)


def test_apply_matrix_equivalence():
    """Test documented equivalence for single rotation:
    `apply(vectors) == vectors @ as_matrix().T.`"""
    r = Rotation.from_rotvec([0, 0, 1])
    # Single vector (3,)
    v = np.array([1.0, 0.0, 0.0])
    xp_assert_close(r.apply(v), v @ r.as_matrix().T)
    # Multiple vectors (P, 3)
    arr = np.array([[1, 0, 0], [1, 2, 3]], dtype=float)
    xp_assert_close(r.apply(arr), arr @ r.as_matrix().T)
    # (3, 3) case: `as_matrix() @ vectors` would not error but give wrong result
    arr33 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
    xp_assert_close(r.apply(arr33), arr33 @ r.as_matrix().T)
    wrong_result = r.as_matrix() @ arr33
    assert not np.allclose(r.apply(arr33), wrong_result)

