
def test__is_dtype_type(input_param, result):
    assert com._is_dtype_type(input_param, lambda tipo: tipo == result)

