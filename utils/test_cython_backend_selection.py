
def test_cython_backend_selection():
    r = Rotation.from_quat(np.array([0, 0, 0, 1]))
    assert r._backend is cython_backend
    r = Rotation.from_quat(np.array([[0, 0, 0, 1]]))
    assert r._backend is cython_backend
    r = Rotation.from_quat(np.array([[[0, 0, 0, 1]]]))
    assert r._backend is xp_backend

