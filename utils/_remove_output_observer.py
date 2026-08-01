
def _remove_output_observer(
    node: Node, model: torch.nn.Module, named_modules: dict[str, torch.nn.Module]
):
    items = list(node.users.items())
    for output_obs_node, _ in items:
        if not _is_activation_post_process_node(output_obs_node, named_modules):
            raise AssertionError(
                "output_obs_node must be an activation post process node"
            )
        output_obs_node.replace_all_uses_with(node)
        model.graph.erase_node(output_obs_node)  # type: ignore[union-attr, operator]

