
def resolve_continuous_batching_config(
    config: PretrainedConfig,
    cb_config: ContinuousBatchingConfig,
    workload_hints: WorkloadHints | None,
    has_logit_processors: bool,
) -> ContinuousBatchingConfig:
    """Returns a deep-copied and fully-resolved `ContinuousBatchingConfig`. The original `cb_config` is not mutated."""
    cb_config = deepcopy(cb_config)

    # Look at whether the user explicitly asked for the decode fast path before we assign a default value
    user_requested_decode_path = cb_config.max_blocks_per_request is not None
    # Same for cuda graphs, if the user signals they want CUDA graphs via any padding/cached-graph parameter
    cuda_graph_requested = any(
        [cb_config.q_padding_interval_size, cb_config.kv_padding_interval_size, cb_config.max_cached_graphs]
    )

    # Resolve missing attributes for which we have hints. Must happen before no-hints resolve.
    resolve_using_hints(cb_config, workload_hints)

    # Resolve remaining missing attributes. Must happen before decode fast path is checked.
    resolve_without_hints(cb_config)

    # Check if the decode fast path is available. Must happen before the compile config.
    ensure_decode_fast_path_is_available(config, cb_config, user_requested_decode_path)

    # Decide if compile should be used. Must happen before CUDA graphs are decided.
    resolve_compile_configs(
        cb_config=cb_config,
        fallback_compile_config=getattr(config, "compile_config", None),
        is_flash_attn=is_flash_attention_requested(config),
        decode_fast_path_available=cb_config.max_blocks_per_request > 0,
    )

    # Decide if CUDA graphs should be used. Should happen after compile configs are decided.
    is_attn_mask_needed = not is_flash_attention_requested(config)
    decide_use_cuda_graphs(
        cb_config=cb_config, is_attn_mask_needed=is_attn_mask_needed, cuda_graph_requested=cuda_graph_requested
    )

    # Decide if asynchronous batching should be used. Should happen after CUDA graphs are decided.
    decide_use_async_batching(cb_config=cb_config, is_attn_mask_needed=is_attn_mask_needed)

    # Resolve the max memory percent. This can happen anytime before cache creation.
    resolve_max_memory_percent(cb_config=cb_config, has_logit_processors=has_logit_processors)
    return cb_config

