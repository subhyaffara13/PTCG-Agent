
def test_unsupported_commontype():
    # linalg gracefully handles unsupported type
    arr = np.array([[1, -2], [2, 5]], dtype='float16')
    with assert_raises_regex(TypeError, "unsupported in linalg"):
        linalg.cholesky(arr)

