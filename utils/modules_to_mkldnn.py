import copy

def modules_to_mkldnn(nodes: list[fx.Node], modules: dict[str, nn.Module]):
    """
    For each node, if it's a module that can be preconverted into MKLDNN,
    then we do so and create a mapping to allow us to convert from the MKLDNN
    version of the module to the original.
    """
    old_modules: dict[nn.Module, nn.Module] = {}
    for node in nodes:
        if node.op == "call_module":
            if not isinstance(node.target, str):
                raise AssertionError(f"Expected str target, got {type(node.target)}")
            cur_module = modules[node.target]
            if type(cur_module) in mkldnn_map:
                # pyrefly: ignore [bad-index, index-error]
                new_module = mkldnn_map[type(cur_module)](cur_module, torch.float)
                if not isinstance(new_module, nn.Module):
                    raise AssertionError(f"Expected nn.Module, got {type(new_module)}")
                old_modules[new_module] = copy.deepcopy(cur_module)
                replace_node_module(node, modules, new_module)
    return old_modules

