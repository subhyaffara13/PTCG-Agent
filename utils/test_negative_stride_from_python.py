
def test_negative_stride_from_python(msg):
    """Eigen doesn't support (as of yet) negative strides. When a function takes an Eigen matrix by
    copy or const reference, we can pass a numpy array that has negative strides.  Otherwise, an
    exception will be thrown as Eigen will not be able to map the numpy array."""

    counting_mat = np.arange(9.0, dtype=np.float32).reshape((3, 3))
    counting_mat = counting_mat[::-1, ::-1]
    second_row = counting_mat[1, :]
    second_col = counting_mat[:, 1]
    np.testing.assert_array_equal(m.double_row(second_row), 2.0 * second_row)
    np.testing.assert_array_equal(m.double_col(second_row), 2.0 * second_row)
    np.testing.assert_array_equal(m.double_complex(second_row), 2.0 * second_row)
    np.testing.assert_array_equal(m.double_row(second_col), 2.0 * second_col)
    np.testing.assert_array_equal(m.double_col(second_col), 2.0 * second_col)
    np.testing.assert_array_equal(m.double_complex(second_col), 2.0 * second_col)

    counting_3d = np.arange(27.0, dtype=np.float32).reshape((3, 3, 3))
    counting_3d = counting_3d[::-1, ::-1, ::-1]
    slices = [counting_3d[0, :, :], counting_3d[:, 0, :], counting_3d[:, :, 0]]
    for ref_mat in slices:
        np.testing.assert_array_equal(m.double_mat_cm(ref_mat), 2.0 * ref_mat)
        np.testing.assert_array_equal(m.double_mat_rm(ref_mat), 2.0 * ref_mat)

    # Mutator:
    with pytest.raises(TypeError) as excinfo:
        m.double_threer(second_row)
    assert (
        msg(excinfo.value)
        == """
        double_threer(): incompatible function arguments. The following argument types are supported:
            1. (arg0: numpy.ndarray[numpy.float32[1, 3], flags.writeable]) -> None

        Invoked with: """
        + repr(np.array([5.0, 4.0, 3.0], dtype="float32"))
    )

    with pytest.raises(TypeError) as excinfo:
        m.double_threec(second_col)
    assert (
        msg(excinfo.value)
        == """
        double_threec(): incompatible function arguments. The following argument types are supported:
            1. (arg0: numpy.ndarray[numpy.float32[3, 1], flags.writeable]) -> None

        Invoked with: """
        + repr(np.array([7.0, 4.0, 1.0], dtype="float32"))
    )

