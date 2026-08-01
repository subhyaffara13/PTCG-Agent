
def pre_compile(
    wrappers: list[CompilerWrapper],
    flat_fn: TraceFn,
    flat_args: list[FxValue],
    flat_args_descs: list[AOTInput],
    aot_config: AOTConfig,
    *,
    fw_metadata: ViewAndMutationMeta,
) -> tuple[TraceFn, list[FxValue], list[AOTInput], ViewAndMutationMeta]:
    """
    Runs a sequence of wrappers on the given function and arguments.
    Mutates wrappers in place.
    """
    for wrapper in wrappers:
        flat_fn, flat_args, flat_args_descs, fw_metadata = wrapper.pre_compile(
            flat_fn, flat_args, flat_args_descs, aot_config, fw_metadata=fw_metadata
        )
    return flat_fn, flat_args, flat_args_descs, fw_metadata

