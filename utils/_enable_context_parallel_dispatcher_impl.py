
def _enable_context_parallel_dispatcher_impl(seq_dim: int, mesh: DeviceMesh) -> None:
    sdpa_cp = _ContextParallel(
        seq_dim=seq_dim,
        attention_type=_ContextParallel.AttentionType.SDPA,
    )

    if _dispatch_mode == _DispatchMode.MONKEY_PATCH:
        _distribute_function(
            F.scaled_dot_product_attention,
            F,
            mesh,
            sdpa_cp.sdpa_input_fn,
            sdpa_cp.sdpa_output_fn,
        )
        _enable_cp_dtensor_dispatcher()
    elif _dispatch_mode == _DispatchMode.MODULE_WRAPPER:
        _enable_cp_dtensor_dispatcher()
    else:
        raise ValueError(f"Unknown dispatch mode: {_dispatch_mode}")

