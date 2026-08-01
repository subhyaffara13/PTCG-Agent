
def update_pointwise_example_value(pointwise_node, input, other, op):
    """
    Update the example value of the add node in the graph to enable followup split cat opt.
    """
    if pointwise_node is not None and hasattr(pointwise_node, "meta"):
        if op is torch.add:
            example_value = torch.add(input, other)
        elif op is torch.mul:
            example_value = torch.mul(input, other)
        else:
            return
        pointwise_node.meta["example_value"] = example_value

