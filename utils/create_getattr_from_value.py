from typing import Any

def create_getattr_from_value(
    module: torch.nn.Module,
    graph: Graph,
    prefix: str,
    value: Any,
    device: torch.device | None = None,
) -> Node:
    """
    Given a value of any type, creates a getattr node corresponding to the value and
    registers the value as a buffer to the module.
    """
    get_new_attr_name = get_new_attr_name_with_prefix(prefix)
    attr_name = get_new_attr_name(module)
    if device is None:
        device = assert_and_get_unique_device(module)
    new_value = (
        value.detach().clone()
        if isinstance(value, torch.Tensor)
        else torch.tensor(value, device=device)
    )
    module.register_buffer(attr_name, new_value)
    # Create get_attr with value
    attr_node = graph.create_node("get_attr", attr_name)
    return attr_node

