
def ensure_decode_fast_path_is_available(
    config: PretrainedConfig, cb_config: ContinuousBatchingConfig, user_requested: bool
) -> None:
    """Ensures the decode fast path is available. If it is not, set the max blocks per request to 0. If it is
    available, and no user-provided max blocks per request, set it to the fallback default."""
    # Then, if the decode fast path is not turned off, check if it is available
    if cb_config.max_blocks_per_request != 0:
        # NOTE: For CUDA, block table should be available with FA2 and FA3, but there seems to be an issue with FA2 atm
        cuda_available = torch.cuda.is_available()
        fa_cuda = is_flash_attention_requested(config, version=3) and cuda_available
        # XPU support is given through its kernel variation `kernels-community/flash-attn2`
        xpu_available = is_torch_xpu_available()
        fa_xpu = is_flash_attention_requested(config, version=2) and xpu_available
        if fa_cuda or fa_xpu:  # Block table is only supported on these
            flash_attn_with_kvcache = lazy_import_paged_flash_attention(config._attn_implementation)[1]
            # Throw a warning only if the decode fast path was requested by the user
            if flash_attn_with_kvcache is None:
                if user_requested:
                    logger.warning(
                        f"Although {cb_config.max_blocks_per_request = }, the decode fast path is not available "
                        f"because `flash_attn_with_kvcache` is not available for {config._attn_implementation = }."
                    )
                cb_config.max_blocks_per_request = 0
        # Specific warning for unsupported attention implementation/device combinations
        else:
            if user_requested:
                logger.warning(
                    f"Although {cb_config.max_blocks_per_request = }, the decode fast path is not available "
                    "because the attention implementation and device combination is not supported. Supported "
                    "combinations are Flash Attention 3 on CUDA, or Flash Attention 2 on XPU through "
                    "`kernels-community/flash-attn2`. "
                    f"Got {config._attn_implementation = }, {cuda_available = }, {xpu_available = }."
                )
            cb_config.max_blocks_per_request = 0

