
def _emit_input_unwrapping(
    state: _CodegenState,
    inp_metas: list[PlainTensorMeta | SubclassCreationMeta],
    frozen_inp_indices: frozenset[int] = frozenset(),
    include_symints: bool = True,
) -> None:
    """Emit unwrapping code for input metas into unwrapped_args.

    Caller must have already emitted ``unwrapped_args = []``.
    """
    for i, meta in enumerate(inp_metas):
        if isinstance(meta, PlainTensorMeta):
            state.emit(f"unwrapped_args.append(args[{i}])")
        elif i in frozen_inp_indices:
            # Frozen by inductor freezing: constant already baked into graph.
            state.emit("unwrapped_args.append(None)")
        else:
            inp_var = state.fresh_name("_inp")
            type_name = state.add_global(
                state.fresh_name("_expected_type"),
                meta.original_subclass_type or type(meta.original_subclass),
            )
            state.emit(f"{inp_var} = args[{i}]")
            state.emit(
                f"assert type({inp_var}) is {type_name}, "
                f"f'expected {{{type_name}}}, got {{type({inp_var})}}'",
            )
            _codegen_unwrap_subclass(
                state, meta, inp_var, indent=1, include_symints=include_symints
            )

