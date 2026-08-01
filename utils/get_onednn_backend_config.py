
def get_onednn_backend_config() -> BackendConfig:
    """
    Return the `BackendConfig` for PyTorch's native ONEDNN backend.
    """
    return (
        BackendConfig("onednn")
        .set_backend_pattern_configs(conv_configs)
        .set_backend_pattern_configs(linear_configs)
        .set_backend_pattern_configs(_get_binary_op_configs(binary_op_dtype_configs))
        .set_backend_pattern_config(_get_cat_config(default_op_dtype_configs))
        .set_backend_pattern_configs(_get_default_op_configs(default_op_dtype_configs))
        .set_backend_pattern_configs(
            _get_fixed_qparams_op_configs(fixed_qparams_op_dtype_configs)
        )
        .set_backend_pattern_configs(
            _get_share_qparams_op_configs(share_qparams_op_dtype_configs)
        )
        .set_backend_pattern_configs(_get_bn_configs(default_op_dtype_configs))
        .set_backend_pattern_configs(_get_ln_configs(layer_norm_op_dtype_configs))
        .set_backend_pattern_configs(_get_rnn_op_configs(rnn_op_dtype_configs))
        .set_backend_pattern_configs(
            _get_embedding_op_configs(embedding_op_dtype_configs)
        )
    )

