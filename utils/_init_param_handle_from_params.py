
def _init_param_handle_from_params(
    state: _FSDPState,
    params: list[nn.Parameter],
    fully_sharded_module: nn.Module,
):
    if len(params) == 0:
        return
    handle = FlatParamHandle(
        params,
        fully_sharded_module,
        state.compute_device,
        SHARDING_STRATEGY_MAP[state.sharding_strategy],
        state.cpu_offload.offload_params,
        state.mixed_precision.param_dtype,
        state.mixed_precision.reduce_dtype,
        state.mixed_precision.keep_low_precision_grads,
        state.process_group,
        state._use_orig_params,
        fsdp_extension=state._fsdp_extension,
    )
    handle.shard()
    if state._handle:
        raise AssertionError("Expected state._handle to be None")
    state.params.append(handle.flat_param)
    state._handle = handle
    state._fully_sharded_module_to_handle[handle._fully_sharded_module] = handle
    cpu_device = torch.device("cpu")
    if state.cpu_offload.offload_params and handle.flat_param.device != cpu_device:
        handle.flat_param_to(cpu_device)

