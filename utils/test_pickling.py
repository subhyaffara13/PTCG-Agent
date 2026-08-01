
def test_pickling(xp):
    # Note: Array API makes no provision for arrays to be pickleable, so
    # it's OK to skip this test for the backends that don't support it
    mat = xp.eye(4)
    mat = xpx.at(mat)[0, 3].set(2.0)
    tf = RigidTransform.from_matrix(mat)
    pkl = pickle.dumps(tf)
    unpickled = pickle.loads(pkl)
    xp_assert_close(tf.as_matrix(), unpickled.as_matrix(), atol=1e-15)


def test_pickling(xp):
    r = Rotation.from_quat(xp.asarray([0, 0, math.sin(np.pi/4), math.cos(np.pi/4)]))
    pkl = pickle.dumps(r)
    unpickled = pickle.loads(pkl)
    xp_assert_close(r.as_matrix(), unpickled.as_matrix(), atol=1e-15)

