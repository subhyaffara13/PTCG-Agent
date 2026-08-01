
def test_tensor_dim(op_name: str) -> int:
    if op_name in test_tensor_dim_ops_1_:
        return 1
    if op_name in test_tensor_dim_ops_2_:
        return 2
    return 3

