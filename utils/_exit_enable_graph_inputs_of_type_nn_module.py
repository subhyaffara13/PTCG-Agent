
def _exit_enable_graph_inputs_of_type_nn_module(
    module_types: set[type[torch.nn.Module]],
) -> None:
    for t in module_types:
        torch._export.utils.deregister_module_as_pytree_input_node(t)

