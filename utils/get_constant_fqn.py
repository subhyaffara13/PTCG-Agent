
def get_constant_fqn(node: torch.fx.Node, constant_name: str) -> str:
    # The FQN of the constant tensor in the state dict should
    # correspond to the module where the constant tensor was
    # originally used.
    if len(node.meta["nn_module_stack"]) == 0:
        return constant_name
    parent_fqn = list(node.meta["nn_module_stack"].values())[-1][0]
    if len(parent_fqn) > 0:
        return f"{parent_fqn}.{constant_name}"
    else:
        return constant_name

