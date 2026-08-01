
def is_B_transposed(gemm_node):  # noqa: N802
    transB_attribute = [attr for attr in gemm_node.attribute if attr.name == "transB"]  # noqa: N806
    if transB_attribute:
        return onnx.helper.get_attribute_value(transB_attribute[0]) > 0

    return False

