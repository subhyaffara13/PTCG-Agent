
def remove_identity(gm: torch.fx.GraphModule) -> torch.fx.GraphModule:
    """
    Removes all identity layers from the module.
    """
    graph = gm.graph
    work_done = False
    for module_name, module in gm.named_modules():
        if type(module) is nn.Identity:
            for node in list(graph.find_nodes(op="call_module", target=module_name)):
                assert len(node.args) == 1
                input_node = node.args[0]
                node.replace_all_uses_with(input_node)
                graph.erase_node(node)
                work_done = True
    if work_done:
        graph.lint()
        gm.recompile()
    return gm

