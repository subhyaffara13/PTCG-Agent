
def get_executorch_backend_config() -> BackendConfig:
    """
    Return the `BackendConfig` for backends PyTorch lowers to through the Executorch stack.
    """
    return (
        BackendConfig("executorch")
        .set_backend_pattern_configs(_get_linear_configs())
        .set_backend_pattern_configs(_get_conv_configs())
        .set_backend_pattern_configs(_get_binary_ops_configs())
        .set_backend_pattern_configs(_get_share_qparams_ops_configs())
        .set_backend_pattern_configs(_get_bn_configs())
        .set_backend_pattern_configs(_get_cat_configs())
        .set_backend_pattern_configs(_get_embedding_op_configs())
    )

