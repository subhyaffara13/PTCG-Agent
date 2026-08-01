
def _copy_graph_attrs(
    gm: torch.fx.GraphModule,
    root_module: UnflattenedModule,
    seen_attrs: dict[str, set[str]],
):
    for child_fqn, names in seen_attrs.items():
        module = _get_attr(root_module, child_fqn) if child_fqn else root_module
        for name in names:
            val = getattr(gm, name)
            setattr(module, name, val)

