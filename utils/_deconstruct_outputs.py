
def _deconstruct_outputs(
    gm: torch.fx.GraphModule,
    signature: ModuleCallSignature,
    module_node: torch.fx.Node,
    node_name_map: dict[str, torch.fx.Node],
    orig_outputs: tuple[torch.fx.Node, ...],
) -> None:
    from .unflatten import _generate_flatten_spec

    flatten_node = _generate_flatten_spec(gm, module_node, signature.out_spec)

    for i, orig_output in enumerate(orig_outputs):
        # Use Proxy to record getitem access.
        proxy_out = torch.fx.Proxy(flatten_node)[i].node  # type: ignore[index]
        orig_output.replace_all_uses_with(proxy_out, propagate_meta=True)

        node_name_map[orig_output.name] = proxy_out

