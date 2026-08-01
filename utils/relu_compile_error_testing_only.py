
def relu_compile_error_TESTING_ONLY(
    gm: torch.fx.GraphModule, example_inputs: list[torch.Tensor]
) -> torch.fx.GraphModule:
    for node in gm.graph.nodes:
        if node.target is torch.relu:
            raise ReluCompileError
    return gm

