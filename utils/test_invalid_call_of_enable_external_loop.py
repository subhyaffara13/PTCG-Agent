
def test_invalid_call_of_enable_external_loop():
    with pytest.raises(ValueError,
                       match='Iterator flag EXTERNAL_LOOP cannot be used'):
        np.nditer(([[1], [2]], [3, 4]), ['multi_index']).enable_external_loop()

