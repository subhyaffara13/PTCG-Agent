
def test_array_view():
    a = np.ones(100 * 4).astype("uint8")
    a_float_view = m.array_view(a, "float32")
    assert a_float_view.shape == (100 * 1,)  # 1 / 4 bytes = 8 / 32

    a_int16_view = m.array_view(a, "int16")  # 1 / 2 bytes = 16 / 32
    assert a_int16_view.shape == (100 * 2,)

