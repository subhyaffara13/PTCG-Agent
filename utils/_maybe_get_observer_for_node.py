
def _maybe_get_observer_for_node(
    node: Node, modules: dict[str, torch.nn.Module]
) -> torch.nn.Module | None:
    """
    If the node is observed, return the observer
    instance. Otherwise, return None.
    """
    for maybe_obs_node in node.users:
        if maybe_obs_node.op == "call_module":
            maybe_obs = modules[str(maybe_obs_node.target)]
            if _is_activation_post_process(maybe_obs):
                return maybe_obs
    return None

