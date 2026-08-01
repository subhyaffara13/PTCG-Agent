
def test_bad_cpp_to_python_casts(m):
    with pytest.raises(
        RuntimeError, match="Cannot use reference internal when there is no parent"
    ):
        m.reference_tensor_internal()

    with pytest.raises(RuntimeError, match="Cannot move from a constant reference"):
        m.move_const_tensor()

    with pytest.raises(
        RuntimeError, match="Cannot take ownership of a const reference"
    ):
        m.take_const_tensor()

    with pytest.raises(
        RuntimeError,
        match="Invalid return_value_policy for Eigen Map type, must be either reference or reference_internal",
    ):
        m.take_view_tensor()

