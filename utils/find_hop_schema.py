
def find_hop_schema(
    gm: torch.fx.GraphModule, target: Target
) -> list[torch._C.FunctionSchema]:
    schemas = []
    for node in gm.graph.find_nodes(op="call_function", target=target):

        def _get_example_value(node: torch.fx.Node) -> Any:
            if node.op == "get_attr":
                if not isinstance(node.target, str):
                    raise AssertionError(
                        f"expected node.target to be str for get_attr, got {type(node.target)}"
                    )
                return getattr(gm, node.target)
            else:
                return (
                    node.meta["example_value"]
                    if "example_value" in node.meta
                    else node.meta["val"]
                )

        fake_args, fake_kwargs = pytree.tree_map_only(
            torch.fx.Node,
            _get_example_value,
            (node.args, node.kwargs),
        )
        schema = node.target.gen_schema(*fake_args, **fake_kwargs)
        schemas.append(schema)
    return schemas

