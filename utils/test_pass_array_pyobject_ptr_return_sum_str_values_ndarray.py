
def test_pass_array_pyobject_ptr_return_sum_str_values_ndarray():
    # Intentionally all temporaries, do not change.
    assert (
        m.pass_array_pyobject_ptr_return_sum_str_values(
            np.array(WrapWithPyValueHolder(-3, "four", 5.0), dtype=object)
        )
        == "-3four5.0"
    )

