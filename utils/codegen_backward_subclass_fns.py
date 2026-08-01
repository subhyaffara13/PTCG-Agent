
def codegen_backward_subclass_fns(
    grad_input_metas: list[PlainTensorMeta | SubclassCreationMeta] | None = None,
) -> tuple[Callable[..., object], Callable[..., object] | None]:
    """Generate codegen'd unwrap and wrap functions for the backward pass.

    Returns (unwrap_fn, wrap_fn). unwrap_fn is used by the backward prologue
    to unwrap non-tangent subclass inputs (always an identity in AOT dispatch
    since the compiled forward operates on unwrapped inner tensors). wrap_fn
    is used by the backward epilogue to wrap flat grad inputs back into
    subclasses; it is None when grad_input_metas is None.
    """
    source = "def unwrap_fn(args):\n    return list(args)"
    globals_dict: dict[str, object] = {}
    unwrap_fn = _compile_and_exec_source(
        source, globals_dict, "unwrap_fn", "backward_subclass_unwrap"
    )

    wrap_fn = None
    if grad_input_metas is not None:
        wrap_source, wrap_globals = _codegen_subclass_wrap_source(grad_input_metas)
        wrap_fn = _compile_and_exec_source(
            wrap_source, wrap_globals, "wrap_fn", "backward_subclass_wrapper"
        )

    return unwrap_fn, wrap_fn

