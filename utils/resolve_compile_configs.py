
def resolve_compile_configs(
    cb_config: ContinuousBatchingConfig,
    fallback_compile_config: CompileConfig | None,
    is_flash_attn: bool,
    decode_fast_path_available: bool,
) -> None:
    """Resolve if the compile configs for varlen and decode paths, modifying these attributes in place if needed.
    Default config use full compile over regional compile, because the throughput is significantly higher (~15%)"""
    default_mode = "max-autotune-no-cudagraphs" if cb_config.default_compile_level >= 2 else "default"
    default_dynamic = cb_config.default_compile_level <= 2
    # For each config, priority is: explicit config, default config, fallback config, None
    if cb_config.varlen_compile_config is None:
        if cb_config.default_compile_level > 0:
            # TODO: now that max_seqlen_k is bucketted, is that still True?
            # We don't use compile with flash varlen, because max_seqlen_k is volatile and introduces recompilations
            if is_flash_attn:
                varlen_config = None
            else:
                varlen_config = CompileConfig(mode=default_mode, fullgraph=True, dynamic=default_dynamic)
        elif fallback_compile_config is not None:
            varlen_config = fallback_compile_config
        else:
            varlen_config = None
    else:
        varlen_config = cb_config.varlen_compile_config

    if cb_config.decode_compile_config is None:
        if cb_config.default_compile_level > 0:
            # Paged attention is wrapped in @torch.compiler.disable so we can't use fullgraph
            decode_config = CompileConfig(mode=default_mode, fullgraph=False, dynamic=default_dynamic)
        elif fallback_compile_config is not None:
            decode_config = fallback_compile_config
        else:
            decode_config = None
    else:
        decode_config = cb_config.decode_compile_config

    # For decode, we throw a warning if the fast decode path is not available and a compile config was found
    if not decode_fast_path_available and cb_config.decode_compile_config is not None:
        decode_config = None
        logger.warning("A decode_compile_config was set but fast decode path is not available. Ignoring it.")

    # Log what will be compiled
    if varlen_config is not None:
        logger.info(f"Varlen path will be compiled with {varlen_config.to_dict()}")
    if decode_config is not None:
        logger.info(f"Decode path will be compiled with {decode_config.to_dict()}")
    # Modify in place
    cb_config.varlen_compile_config = varlen_config
    cb_config.decode_compile_config = decode_config

