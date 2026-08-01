
def decide_use_cuda_graphs(
    cb_config: ContinuousBatchingConfig, is_attn_mask_needed: bool, cuda_graph_requested: bool
) -> None:
    """Decides whether or not to use cuda graphs for continuous batching. If the user specified this in the config
    or if they specified a parameter related to cuda graphs, they are turned on. Otherwise, we use a heuristic
    based on the attention implementation: we turn on cuda graphs if and only if no attention mask is needed.

    This function modifies the `use_cuda_graph` attribute of the config in place, to a tuple of booleans.
    """
    # If cuda is not available, we cannot use cuda graphs
    if not torch.cuda.is_available():
        intended_use_cuda_graph = any(cb_config.cuda_graph_booleans)
        if intended_use_cuda_graph:  # throw a warning only if the user intended to use cuda graphs
            logger.warning(
                f"{cb_config.use_cuda_graph = } but {torch.cuda.is_available() = }: turning off cuda graphs"
            )
        cb_config.use_cuda_graph = (False, False)

    # Else if use_cuda_graph is specified, we follow the user's choice and make sure it is a tuple of booleans
    elif cb_config.use_cuda_graph is not None:
        if isinstance(cb_config.use_cuda_graph, bool):
            cb_config.use_cuda_graph = (cb_config.use_cuda_graph, cb_config.use_cuda_graph)

    # Else if the user specified a parameter related to cuda graphs, we activate cuda graphs
    elif cuda_graph_requested:
        cb_config.use_cuda_graph = (True, True)

    # Otherwise we have a default heuristic based on the attention implementation:
    # attention implementations where an attention mask is needed suffer a lot more from the padding associated
    # with cuda graphs, so default is to turn cuda graphs off for those implementations
    else:
        use_cuda_graph = []
        for compile_config in [cb_config.varlen_compile_config, cb_config.decode_compile_config]:
            # No compile config means we decide on attention
            if compile_config is None:
                use_cuda_graph.append(not is_attn_mask_needed)
                continue
            # Otherwise we disable cuda graphs if the compile config uses them
            options = torch._inductor.list_mode_options().get(compile_config.mode, compile_config.options)
            compile_uses_cudagraphs = options.get("triton.cudagraphs", False)
            if compile_uses_cudagraphs:
                logger.warning(
                    f"Compile config {compile_config.mode = } uses cudagraphs, which usually does not work well with "
                    "continuous batching. We recommend using mode 'default' or 'max-autotune-no-cudagraphs' instead."
                )
            use_cuda_graph.append(not compile_uses_cudagraphs and not is_attn_mask_needed)
        cb_config.use_cuda_graph = tuple(use_cuda_graph)

    logger.info(f"Using cuda graphs for (varlen, decode) paths: {cb_config.use_cuda_graph}")

