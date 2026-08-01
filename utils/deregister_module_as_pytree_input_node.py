
def deregister_module_as_pytree_input_node(cls: type[torch.nn.Module]) -> None:
    _deregister_pytree_node(cls)
    _deregister_pytree_flatten_spec(cls)

