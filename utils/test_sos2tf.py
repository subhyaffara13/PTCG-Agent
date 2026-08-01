
def test_sos2tf():
    sos_f32 = np.array([[4, 5, 6, 1, 2, 3]], dtype=np.float32)
    b, a = sos2tf(sos_f32)
    assert b.dtype == np.float32
    assert a.dtype == np.float32

