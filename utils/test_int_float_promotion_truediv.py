
def test_int_float_promotion_truediv(fscalar):
    # Promotion for mixed int and float32/float16 must not go to float64
    i = np.int8(1)
    f = fscalar(1)
    expected = np.result_type(i, f)
    assert (i / f).dtype == expected
    assert (f / i).dtype == expected
    # But normal int / int true division goes to float64:
    assert (i / i).dtype == np.dtype("float64")
    # For int16, result has to be ast least float32 (takes ufunc path):
    assert (np.int16(1) / f).dtype == np.dtype("float32")

