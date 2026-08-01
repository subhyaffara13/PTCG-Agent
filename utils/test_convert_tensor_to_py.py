
def test_convert_tensor_to_py(m, func_name):
    writeable = func_name in assert_equal_funcs
    assert_equal_tensor_ref(getattr(m, func_name)(), writeable=writeable)

