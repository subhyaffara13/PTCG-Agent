from typing import Any

def snode_args_kwargs(snode: BaseSchedulerNode) -> tuple[list[Any], dict[str, Any]]:
    args = snode.node.inputs  # type: ignore[union-attr]
    args = snode.node.fill_non_provided_args(  # type: ignore[union-attr]
        [*args, *snode.node.constant_args],  # type: ignore[union-attr]
        snode.node.kwargs,  # type: ignore[union-attr]
    )
    kwargs = snode.node.kwargs  # type: ignore[union-attr]
    flat_args, flat_args_pytree_spec = pytree.tree_flatten((args, kwargs))

    def _is_tensor_ir(x) -> bool:  # type: ignore[no-untyped-def]
        return isinstance(x, torch._inductor.ir.IRNode) and not isinstance(
            x,
            (torch._inductor.ir.GeneratorState, torch._inductor.ir.OpaqueObjectState),
        )

    flat_args = [
        torch._inductor.ir.ir_node_to_tensor(a, replace_symbols_with_hints=True)
        if _is_tensor_ir(a)
        else a
        for a in flat_args
    ]

    def _tensor(size, dtype, device) -> torch.Tensor:  # type: ignore[no-untyped-def]
        return torch.empty(size, dtype=dtype, device=device)

    def to_real_tensor(e: Any) -> Any:
        if not isinstance(e, torch.Tensor):
            return e
        out = _tensor(e.size(), e.dtype, e.device)
        return out

    flat_args = [to_real_tensor(a) for a in flat_args]
    args, kwargs = pytree.tree_unflatten(flat_args, flat_args_pytree_spec)
    return args, kwargs

