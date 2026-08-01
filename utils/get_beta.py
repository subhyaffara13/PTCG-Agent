
def get_beta(gemm_node):
    beta_attribute = [attr for attr in gemm_node.attribute if attr.name == "beta"]
    if beta_attribute:
        return onnx.helper.get_attribute_value(beta_attribute[0])

    return 1.0

