
def test_pass_array_pyobject_ptr_return_sum_str_values_list():
    # Intentionally all temporaries, do not change.
    assert (
        m.pass_array_pyobject_ptr_return_sum_str_values(
            WrapWithPyValueHolder(2, "three", -4.0)
        )
        == "2three-4.0"
    )

