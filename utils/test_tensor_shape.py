
def test_tensor_shape(op_name: str) -> str:
    if op_name in test_tensor_shape_json:
        return test_tensor_shape_json[op_name]
    else:
        return ""

