
def get_estimate_runtime_cache_key_from_snode(snode: BaseSchedulerNode) -> str:
    python_kernel_name = getattr(snode.node, "python_kernel_name", "")
    args = snode.node.inputs  # type: ignore[union-attr]
    args = snode.node.fill_non_provided_args(  # type: ignore[union-attr]
        [*args, *snode.node.constant_args],  # type: ignore[union-attr]
        snode.node.kwargs,  # type: ignore[union-attr]
    )
    kwargs = snode.node.kwargs  # type: ignore[union-attr]
    flat_args, flat_args_pytree_spec = pytree.tree_flatten((args, kwargs))

    def _is_tensor_ir(x) -> bool:  # type: ignore[no-untyped-def]
        return isinstance(x, ir.IRNode) and not isinstance(
            x, (ir.GeneratorState, ir.OpaqueObjectState)
        )

    cache_key = str(
        (python_kernel_name,)
        + tuple(tuple(a.get_size()) if _is_tensor_ir(a) else None for a in flat_args)
    )
    return cache_key

