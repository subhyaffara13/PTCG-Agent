
def update_stack_example_value(node, metadata, dim=0, op=torch.stack):
    """
    Update the example value of the node in the graph to enable followup split cat opt.
    """
    if node is not None and hasattr(node, "meta"):
        if op is torch.stack:
            example_value = torch.stack(metadata, dim=dim)
        elif op is torch.unbind:
            example_value = torch.unbind(metadata, dim=dim)  # type: ignore[assignment]
        else:
            return
        node.meta["example_value"] = example_value

