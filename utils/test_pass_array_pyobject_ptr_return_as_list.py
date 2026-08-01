
def test_pass_array_pyobject_ptr_return_as_list():
    # Intentionally all temporaries, do not change.
    assert UnwrapPyValueHolder(
        m.pass_array_pyobject_ptr_return_as_list(
            np.array(WrapWithPyValueHolder(-1, "two", 3.0), dtype=object)
        )
    ) == [-1, "two", 3.0]

