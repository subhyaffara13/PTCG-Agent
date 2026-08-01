
def dispatch_trace(
    root: Module | Callable[..., Any],
    tracer: Tracer,
    concrete_args: tuple[object, ...] | None = None,
) -> GraphModule:
    graph = tracer.trace(root, concrete_args)  # type: ignore[arg-type]

    # NB: be careful not to DCE .item() calls
    def impure_pred(n: fx.Node) -> bool:
        from .symbolic_shapes import is_accessor_node

        # Always defer to the built-in notion of impure
        if n.is_impure():
            return True

        # Accessors always OK to DCE
        if is_accessor_node(n):
            return False

        # If the operator in question takes SymInt args to SymInt output,
        # we assume it's pure and OK to DCE
        if (
            isinstance(n.meta.get("val"), py_sym_types)
            and
            # NB: constant args ok
            all(
                isinstance(a.meta.get("val"), py_sym_types)
                for a in n.args
                if isinstance(a, fx.Node)
            )
        ):
            return False

        # No idea, just assume it's not OK
        return True

    graph.eliminate_dead_code(impure_pred)
    from torch._inductor.fx_passes.dedupe_symint_uses import dedupe_symints

    dedupe_symints(graph)
    name = root.__class__.__name__ if isinstance(root, Module) else root.__name__
    return fx._lazy_graph_module._make_graph_module(tracer.root, graph, name)

