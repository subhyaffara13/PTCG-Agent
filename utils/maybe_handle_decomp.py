
def maybe_handle_decomp(
    proxy_mode: ProxyTorchDispatchMode,
    op: OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    from torch._inductor.compiler_bisector import CompilerBisector

    decomp_table = CURRENT_DECOMPOSITION_TABLE.get({})
    if op in decomp_table:
        if CompilerBisector.disable_subsystem(
            "aot_eager_decomp_partition", "decomposition", lambda: repr(op)
        ):
            return NotImplemented

        with proxy_mode:
            proxy_mode.decomp_layers += 1
            out = decomp_table[op](*args, **kwargs)
            proxy_mode.decomp_layers -= 1
            return out

    return NotImplemented

