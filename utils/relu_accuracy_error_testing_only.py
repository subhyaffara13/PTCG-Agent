
def relu_accuracy_error_TESTING_ONLY(
    gm: torch.fx.GraphModule, example_inputs: list[torch.Tensor]
) -> torch.fx.GraphModule:
    for node in gm.graph.nodes:
        if node.target is torch.relu:
            node.target = torch.add
            node.args = (node.args[0], 1)
    gm.recompile()

    return gm

