
def gather_origins(
    args: Sequence[IRNode], kwargs: dict[str, IRNode]
) -> OrderedSet[torch.fx.Node]:
    from . import ir

    def is_unrealized_node(n: IRNode) -> bool:
        if isinstance(n, ir.TensorBox):
            return is_unrealized_node(n.data)
        if isinstance(n, ir.StorageBox):
            return is_unrealized_node(n.data)
        return isinstance(n, ir.IRNode) and not isinstance(
            n,
            (
                ir.ComputedBuffer,
                ir.InputsKernel,
                ir.InputBuffer,
                ir.TemplateBuffer,
            ),
        )

    # kwargs and args may include a container of node, for example torch.cat([t1, t2])
    # flatten them before search the unrealized nodes
    kwargs_flatten, _ = tree_flatten(kwargs)
    kwargs_origins = [val.origins for val in kwargs_flatten if is_unrealized_node(val)]
    args_flatten, _ = tree_flatten(args)
    args_origins = [val.origins for val in args_flatten if is_unrealized_node(val)]
    return OrderedSet(itertools.chain(*args_origins, *kwargs_origins))

