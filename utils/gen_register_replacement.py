
def gen_register_replacement(
    unique_name: str,
    search_fn: SearchFn,
    replace_fn: ReplaceFn,
    example_inputs: Iterable[Any],
    trace_fn: TraceFn,
    pass_dicts: _PassDictsType | Sequence[_PassDictsType],
    extra_check: Callable[[Match], bool] = _return_true,
    scalar_workaround: dict[str, float | int] | None = None,
    exclusive_arg_names: Sequence[str] = (),
    skip_duplicates: bool = False,
    get_decomp_fn: Callable[..., dict[Any, Callable[..., Any]]] = select_decomp_table,
) -> None:
    # Make sure the example_inputs is materialized.
    example_inputs = tuple(example_inputs)

    if "PYTORCH_GEN_PATTERNS" in os.environ:
        pat = _serialize_pattern(
            unique_name, search_fn, example_inputs, trace_fn, scalar_workaround
        )
    else:
        pattern_name = search_fn.__name__
        m = importlib.import_module(
            f"torch._inductor.fx_passes.serialized_patterns.{pattern_name}"
        )
        if not m or not hasattr(m, unique_name):
            log.warning(
                "Precompiled pattern %r not found. Run torchgen/fuse/gen_patterns.py.",
                unique_name,
            )
        pat = getattr(m, unique_name)

    for arg in pytree.tree_iter(example_inputs):
        if isinstance(arg, FakeTensor) and arg.constant is not None:
            # This can be a problem - small fake tensors (e.g. `tensor(2)`) will
            # hold onto their original constant value - and by stashing it here
            # will cause a memory leak if the constant value is on GPU.
            # Since this is just an optimization we can clear it out.
            arg.constant = None

    _known_precompiled_patterns.append(
        (search_fn, example_inputs, trace_fn, scalar_workaround, pat)
    )
    register_replacement(
        search_fn,
        replace_fn,
        example_inputs,
        trace_fn,
        pass_dicts,
        extra_check,
        scalar_workaround,
        exclusive_arg_names,
        search_fn_pattern=pat,
        skip_duplicates=skip_duplicates,
        pattern_name=unique_name,
        get_decomp_fn=get_decomp_fn,
    )

