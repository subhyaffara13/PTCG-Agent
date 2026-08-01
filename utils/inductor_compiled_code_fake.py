
def inductor_compiled_code_fake(func, inputs, *, name=None):
    resolved = _resolve_inductor_callable(func)
    if resolved.original_gm is None:
        raise RuntimeError(
            "inductor_compiled_code original_gm is None — the compiled graph may "
            "have been serialized without it. Recompile to restore."
        )
    # Run the original FX graph under FakeTensorMode to re-derive output
    # shapes, dtypes, and aliasing from the input fake tensors.
    return tuple(resolved.original_gm(*inputs))

