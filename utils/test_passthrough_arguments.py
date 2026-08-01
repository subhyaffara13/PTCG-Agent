
def test_passthrough_arguments(doc):
    assert doc(m.vec_passthrough) == (
        "vec_passthrough("
        + ", ".join(
            [
                "arg0: float",
                "arg1: numpy.ndarray[numpy.float64]",
                "arg2: numpy.ndarray[numpy.float64]",
                "arg3: numpy.ndarray[numpy.int32]",
                "arg4: int",
                "arg5: m.numpy_vectorize.NonPODClass",
                "arg6: numpy.ndarray[numpy.float64]",
            ]
        )
        + ") -> object"
    )

    b = np.array([[10, 20, 30]], dtype="float64")
    c = np.array([100, 200])  # NOT a vectorized argument
    d = np.array([[1000], [2000], [3000]], dtype="int")
    g = np.array([[1000000, 2000000, 3000000]], dtype="int")  # requires casting
    assert np.all(
        m.vec_passthrough(1, b, c, d, 10000, m.NonPODClass(100000), g)
        == np.array(
            [
                [1111111, 2111121, 3111131],
                [1112111, 2112121, 3112131],
                [1113111, 2113121, 3113131],
            ]
        )
    )

