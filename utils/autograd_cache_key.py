
def autograd_cache_key(
    graph,
    example_inputs,
    ignore_shape_env: bool,
    decompositions,
    compiler_config_extra: CompilerConfigExtra,
    keep_inference_input_mutations: bool = False,
    disable_functionalization: bool = False,
):
    (
        _params_buffers_flat,
        _params_spec,
        _buffers_spec,
        full_args,
        _full_args_descs,
        aot_config,
    ) = prepare_aot_config(
        graph,
        example_inputs,
        decompositions,
        keep_inference_input_mutations,
        ignore_shape_env,
        force_non_lazy_backward_lowering=config.force_non_lazy_backward_lowering,
        disable_functionalization=disable_functionalization,
    )

    fake_mode, shape_env = construct_fake_mode(full_args, aot_config)
    fake_flat_args, _act_input_indices = process_inputs(
        full_args, aot_config, fake_mode, shape_env, ignore_shape_env
    )

    return autograd_cache.autograd_cache_key(
        graph, fake_flat_args, aot_config, compiler_config_extra
    )


def autograd_cache_key(
    graph,
    example_inputs,
    ignore_shape_env: bool,
    decompositions=None,
):
    if config.cpp_wrapper or config.fx_wrapper:
        raise RuntimeError(
            "autograd_cache_key is not supported with cpp_wrapper or fx_wrapper"
        )

    decompositions = (
        decompositions if decompositions is not None else select_decomp_table()
    )
    # compile_fx applies these graph transforms before reaching _compile_fx_main.
    # Neither occurs on the torch.compile/Dynamo path (which always produces
    # tuple-returning, pre-flattened graphs). Not supported by this API.
    if isinstance(graph, GraphModule) and not graph_returns_tuple(graph):
        raise NotImplementedError(
            "autograd_cache_key does not support graphs that don't return a tuple"
        )
    if any(isinstance(x, (list, tuple, dict)) for x in example_inputs):
        raise NotImplementedError(
            "autograd_cache_key does not support nested container inputs"
        )

    compiler_config_extra = create_compiler_config_extra(graph)

    # These context managers replicate the ones that _compile_fx_main sets up
    # before calling aot_autograd, so that the config snapshot captured by
    # autograd_cache_key is identical to a real compile_fx run:
    #   _compile_fx_main outer with-block: _use_lazy_graph_module,
    #       enable_python_dispatcher, preserve_node_meta,
    #       reset_provenance_globals
    #   _compile_fx_main aot_autograd with-block: V.set_fake_mode,
    #       torch._guards.tracing, compiled_autograd._disable,
    #       functorch_config.patch

    fake_mode = detect_fake_mode(example_inputs) or torch._subclasses.FakeTensorMode(
        allow_non_fake_inputs=True
    )
    tracing_context = (
        torch._guards.TracingContext.try_get()
        or torch._guards.TracingContext(fake_mode)
    )

    with (
        functorch_config.patch(
            unlift_effect_tokens=True, selective_decompose=config.selective_decompose
        ),
        _use_lazy_graph_module(dynamo_config.use_lazy_graph_module),
        enable_python_dispatcher(),
        torch.fx.traceback.preserve_node_meta(
            config.trace.provenance_tracking_level == 1
        ),
        torch._inductor.debug.reset_provenance_globals(),
        V.set_fake_mode(fake_mode),
        torch._guards.tracing(tracing_context),
        compiled_autograd._disable(),
    ):
        return aot_autograd.autograd_cache_key(
            graph,
            example_inputs,
            ignore_shape_env=ignore_shape_env,
            decompositions=decompositions,
            compiler_config_extra=compiler_config_extra,
            keep_inference_input_mutations=True,
        )


def autograd_cache_key(
    graph,
    example_inputs,
    dynamic_shapes: Any,
    aot: bool = False,  # AOT mode, which uses BundledAOTAutogradCache
):
    from . import compile_fx

    ignore_shape_env = _resolve_ignore_shape_env(dynamic_shapes)
    with _standalone_context(graph, dynamic_shapes, aot):
        return compile_fx.autograd_cache_key(
            graph,
            example_inputs,
            ignore_shape_env=ignore_shape_env,
        )


def autograd_cache_key(
    mod: torch.fx.GraphModule | torch._dynamo.utils.GmWrapper,
    example_inputs: Sequence[Any],
    config: AOTConfig,
    compiler_config_extra: CompilerConfigExtra | None = None,
    # TODO: add args and parameters
) -> tuple[str, list[str]]:
    """
    Generate a unique hash of the FX graph for caching.
    """

    gm = mod.gm if isinstance(mod, torch._dynamo.utils.GmWrapper) else mod
    with sanitize_gm_for_cache(gm):
        try:
            check_cacheable(gm)
            if has_triton_package():
                # Due to https://github.com/triton-lang/triton/issues/3729,
                # if triton is < 3.2.0, AOTAutogradCache may cause us to
                # attempt to load a cache entry without initializing
                # the CUDA context on the autograd thread.

                # Without caching, we naturally do this initialization when
                # tracing through the graph with the autograd engine.
                import triton

                if triton.__version__ < "3.2.0":
                    raise BypassAOTAutogradCache(
                        "AOTAutogradCache requires triton 3.2.0"
                    )
            details = AOTAutogradCacheDetails(
                gm, example_inputs, config, create_fx_config(compiler_config_extra)
            )
            pickler = AOTAutogradCachePickler(gm)
            # The prefix distinguishes among the other kinds of objects we cache
            key = "a" + pickler.get_hash(details)
            # debug_lines re-hashes every attribute individually and is
            # expensive. Only compute when debug logging is enabled.
            if log.isEnabledFor(logging.DEBUG):
                debug_lines = pickler.debug_lines(details)
                log.debug(
                    "Autograd graph cache hash details for key %s:\n%s",
                    key,
                    LazyString(lambda: "\n".join(debug_lines)),
                )
            else:
                debug_lines: list[str] = []
            return key, debug_lines
        except Exception:
            # If enable_aot_compile is set, we're in AOT precompile mode where we always
            # want to use fallback nonce keys. Unlike caching, it's fine if we can't generate
            # a proper key because we are guaranteed in an AOT precompile world users are in
            # complete control of distributing and loading artifacts.
            if torch._functorch.config.bypass_autograd_cache_key:
                log.info(
                    "Failed to generate AOTAutograd cache key; falling back to nonce due to enable_aot_compile",
                    exc_info=True,
                )
                return str(random.random()), []
            else:
                raise

