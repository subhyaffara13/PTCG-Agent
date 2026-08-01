
def set_default_beta(gemm_node):
    beta_attribute = [attr for attr in gemm_node.attribute if attr.name == "beta"]
    if beta_attribute:
        beta_attribute[0].f = 1.0

    return 1.0

