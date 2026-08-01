
def test_numpy_float32_inputs():
    Rotation.from_quat(np.array([1, 0, 0, 0], dtype=np.float32))

