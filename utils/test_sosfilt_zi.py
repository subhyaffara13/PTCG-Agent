
def test_sosfilt_zi():
    sos_f32 = np.array([[4, 5, 6, 1, 2, 3]], dtype=np.float32)
    assert sosfilt_zi(sos_f32).dtype == np.float32

