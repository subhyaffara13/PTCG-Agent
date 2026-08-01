
def _register_constants_as_buffers(
    mod: torch.fx.GraphModule, state_dict, non_persistent_buffers
):
    # TODO some annoying circular dependency issue
    from torch.export.unflatten import _assign_attr, _AttrKind

    temp_registered_constants = set()

    for node in mod.graph.nodes:
        if node.op == "get_attr":
            target = torch.fx.graph_module._get_attr(mod, node.target)
            if isinstance(target, torch.Tensor):
                # Make sure we also check if the original buffer is
                # non persistent as well.
                if (node.target not in state_dict) and (
                    node.target not in non_persistent_buffers
                ):
                    torch.fx.graph_module._del_attr(mod, node.target)
                    _assign_attr(target, mod, node.target, _AttrKind.BUFFER, False)
                    temp_registered_constants.add(node.target)

    mod.recompile()

    return temp_registered_constants

