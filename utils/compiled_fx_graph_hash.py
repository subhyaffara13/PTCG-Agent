
def compiled_fx_graph_hash(
    gm: torch.fx.GraphModule,
    example_inputs: Sequence[InputType],
    fx_kwargs: _CompileFxKwargs,
    inputs_to_check: Sequence[int],
) -> tuple[str, list[str]]:
    """
    Generate a unique hash of the FX graph for caching.
    """
    details = FxGraphHashDetails(gm, example_inputs, fx_kwargs, inputs_to_check)
    has_user_defined_triton_kernels = len(details.user_defined_triton_source) != 0
    pickler = FxGraphCachePickler(gm, has_user_defined_triton_kernels)

    # The prefix distinguishes among the other kinds of objects we
    # cache in this module.
    key = "f" + pickler.get_hash(details)
    debug_lines = pickler.debug_lines(details)
    debug_str = "\n".join(debug_lines)
    log.debug(f"FX graph cache hash details for key {key}:\n{debug_str}")  # noqa: G004
    return key, debug_lines

