
def _is_output_dtype_supported_by_backend(
    node: Node,
    qconfig: QConfigAny,
    dtype_config: DTypeConfig,
) -> bool:
    """Check if the configured qconfig for the output
    is supported by the backend or not
    """
    # TODO: move dtype check into `_qconfig_satisfies_dtype_config_constraints` as well
    backend_config_output_dtype = dtype_config.output_dtype
    # TODO: we should check is_dynamic here as well, the code from _is_input_arg_dtype_supported_by_backend
    # from input activation check can be reused here
    qconfig_output_dtype = None
    output_act_obs_or_fq_ctr = node.meta["target_dtype_info"].get(
        "output_act_obs_or_fq_ctr", _DEFAULT_FP32_OBS_OR_FQ_CTR
    )
    output_act_obs_or_fq = (
        output_act_obs_or_fq_ctr() if output_act_obs_or_fq_ctr else None
    )
    qconfig_output_dtype, qconfig_output_is_dynamic = _get_dtype_and_is_dynamic(
        output_act_obs_or_fq
    )
    # TODO: this is a hack because we can only specify one activation_obs_or_fq for
    # qconfig (qconfig.activation), and we are only supporting dynamically quantized
    # linear op which has fp32 output dtype, this should be removed if we generalize
    # the structure of qconfig in the future
    if qconfig_output_is_dynamic:
        qconfig_output_dtype = torch.float32
    dtype_matches = qconfig_output_dtype == backend_config_output_dtype
    qconfig_satisfies_constraints = _qconfig_satisfies_dtype_config_constraints(
        qconfig, dtype_config.output_dtype_with_constraints
    )
    return backend_config_output_dtype is None or (
        dtype_matches and qconfig_satisfies_constraints
    )

