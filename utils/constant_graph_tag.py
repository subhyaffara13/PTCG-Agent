
def constant_graph_tag(
    gm: torch.fx.GraphModule,
    skip_constructors: bool = True,
    lifted_constant_names: list[str] | None = None,
    skip_folding_node_fn: Callable[[torch.fx.Node], bool] | None = None,
) -> None:
    with torch.utils._python_dispatch._disable_current_modes():
        cf = ConstantFolder(
            gm,
            skip_constructors=skip_constructors,
            lifted_constant_names=lifted_constant_names,
            skip_folding_node_fn=skip_folding_node_fn,
        )
        cf.run()

        for node in gm.graph.nodes:
            if skip_folding_node_fn is not None and skip_folding_node_fn(node):
                node.meta[META_TAG] = MODULE_TAG
                continue
            if (
                is_const_source(node, lifted_constant_names)
                or node in cf.node_replacements
                or node in cf.replaced_uses
            ):
                node.meta[META_TAG] = CONST_MODULE_TAG
            else:
                node.meta[META_TAG] = MODULE_TAG


def constant_graph_tag(gm: torch.fx.GraphModule) -> None:
    with torch.utils._python_dispatch._disable_current_modes():
        cf = ConstantFolder(gm, skip_constructors=True)
        cf.run()

        for node in gm.graph.nodes:
            if (
                node.op == "get_attr"
                or node in cf.node_replacements
                or node in cf.replaced_uses
            ):
                node.meta[META_TAG] = CONST_MODULE_TAG
            else:
                node.meta[META_TAG] = MODULE_TAG

