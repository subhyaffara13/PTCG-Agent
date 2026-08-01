
def aot_function(
    fn: Callable[_P, _R],
    fw_compiler: AOTDispatchCompiler,
    bw_compiler: AOTDispatchCompiler | None = None,
    partition_fn: Callable[..., Any] = default_partition,
    decompositions: dict[OpOverload, Callable[..., Any]] | None = None,
    num_params_buffers: int = 0,
    keep_inference_input_mutations: bool = False,
    inference_compiler: AOTDispatchCompiler | None = None,
    *,
    # Whether or not to trace with dynamic shapes
    dynamic: bool = False,
    enable_log: bool = True,
    disable_functionalization: bool = False,
    _disable_torch_fn_metadata_mode: bool = False,
) -> Callable[_P, Any]:
    """
    Traces the forward and backward graph of :attr:`fn` using torch dispatch
    mechanism, and then compiles the generated forward and backward graphs
    through :attr:`fw_compiler` and :attr:`bw_compiler`.

    :func:`aot_function` traces the forward and backward graph ahead of time,
    and generates a joint forward and backward graph.  :attr:`partition_fn` is
    then used to separate out forward and backward graphs. The partitioner
    function can be used to perform optimizations such as recomputation. One can
    set `decompositions` dictionary to decompose the operators into a sequence
    of core or simpler operators supported by the backend compilers.

    .. warning::
        This API is experimental and likely to change.

    Args:
        fn (Callable): A Python function that takes one or more arguments. Must
            return one or more Tensors.
        fw_compiler (Callable): A Python function that accepts an Fx graph with
            Aten ops and input args, and returns a Callable that semantically is
            equivalent to the input Fx graph.
        bw_compiler (Optional[Callable]): A Python function that accepts an
            Fx graph with Aten ops and input args, and returns a Callable that
            semantically is equivalent to the input Fx graph.  Default: None
            (when None, it defaults to the :attr:`fw_compiler`)
        partition_fn (Callable): A Python function that takes a joint forward
            and backward graph, and partitions it into separate forward and
            backward graphs.
        decompositions (Dict): A dictionary to define the decomposition of
            larger Aten ops into simpler or core Aten ops.
        inference_compiler (Optional[Callable]): A Python function that accepts an
            Fx graph with Aten ops and input args, and returns a Callable that
            semantically is equivalent to the input Fx graph. inference_compiler is invoked
            if no autograd is needed. Default: None
            (when None, it defaults to the :attr:`fw_compiler`)
    Returns:
        Returns a ``Callable`` that retains the eager behavior of the original
        :attr:`fn`, but with forward and backward graph compiled via
        :attr:`fw_compile` and :attr:`bw_compile`.

    A simple example usage of :func:`aot_function` is as follows. This example
    will print the forward and backward graphs of the function ``fn``

        >>> fn = lambda x: x.sin().cos()
        >>> def print_compile_fn(fx_module, args):
        >>>     print(fx_module)
        >>>     return fx_module
        >>> aot_fn = aot_function(fn, print_compile_fn)
        >>> x = torch.randn(4, 5, requires_grad=True)
        >>> aot_fn(x)
    """

    aot_config = AOTConfig(
        fw_compiler=None,
        bw_compiler=None,
        inference_compiler=None,
        partition_fn=None,
        decompositions=decompositions,
        num_params_buffers=num_params_buffers,
        aot_id=next(AOT_COUNTER),
        keep_inference_input_mutations=keep_inference_input_mutations,
        dynamic_shapes=dynamic,
        aot_autograd_arg_pos_to_source=None,
        is_export=False,
        no_tangents=False,
        enable_log=enable_log,
        disable_functionalization=disable_functionalization,
        _disable_torch_fn_metadata_mode=_disable_torch_fn_metadata_mode,
    )
    cached_res = None

    @wraps(fn)
    def returned_function(*args: _P.args, **kwargs: _P.kwargs) -> Any:
        nonlocal cached_res
        # Now flatten the tensor args
        flat_args = pytree.arg_tree_leaves(*args, **kwargs)

        # Compile the function and save it in the cache
        if cached_res is None:
            flat_fn, out_spec = create_tree_flattened_fn(fn, args, kwargs)
            (fake_mode, shape_env) = construct_fake_mode(flat_args, aot_config)
            fake_flat_args: FakifiedFlatArgs
            fake_flat_args, act_input_indices = process_inputs(
                flat_args, aot_config, fake_mode, shape_env
            )
            # TODO: We actually could use the pytree path to make better descs.
            # Also, the descs here are bad if you do aot_module.
            fake_flat_args_descs: list[AOTInput] = [
                PlainAOTInput(i) for i in range(len(fake_flat_args))
            ]
            with contextlib.ExitStack() as stack:
                aot_state = create_aot_state(
                    stack,
                    flat_fn,
                    fake_flat_args,
                    fake_flat_args_descs,
                    aot_config,
                    fake_mode,
                    shape_env,
                )
                aot_state.fw_metadata.act_input_indices = act_input_indices
                aot_graph_capture = aot_stage1_graph_capture(aot_state, flat_fn)
                compiled_fn, _ = aot_stage2_compile(
                    aot_state,
                    aot_graph_capture,
                    partition_fn,
                    fw_compiler,
                    bw_compiler,
                    inference_compiler,
                )
            cached_res = (compiled_fn, out_spec)

        cached_fn, out_spec = cached_res
        out = cached_fn(flat_args)
        return out_spec.unflatten(out)

    return returned_function

