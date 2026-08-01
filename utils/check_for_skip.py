
def check_for_skip(aot_model: torch.fx.GraphModule, num_fixed: int) -> str | None:
    if not config.cudagraph_backend_support_input_mutation:
        if mut_skip := check_for_mutation_ignore_cuda_graph_managed_tensor(
            aot_model, num_fixed
        ):
            return mut_skip

    if skip := check_multiple_devices_or_any_cpu_nodes(
        get_device_node_mapping(aot_model)
    ):
        return skip

    if node := get_first_incompatible_cudagraph_node(aot_model):
        return format_default_skip_message(f"incompatible op ({node.name})")

    return None

