
def test_cast_numpy_int64_to_uint64():
    m.function_taking_uint64(123)
    m.function_taking_uint64(np.uint64(123))

