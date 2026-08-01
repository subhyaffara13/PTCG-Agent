
def _get_pattern_output_dtype(match: Match):
    """
    Get the pattern's output dtype from node's meta
    Assume only 1 output node in this matched pattern.
    """
    pattern_output_nodes = match.output_nodes()
    assert len(pattern_output_nodes) == 1
    output_node = pattern_output_nodes[0]
    assert isinstance(output_node, torch.fx.Node)
    output_dtype = output_node.meta["val"].dtype
    assert output_dtype in [
        torch.int8,
        torch.uint8,
        torch.float32,
        torch.bfloat16,
        torch.float8_e4m3fn,
    ]
    return output_dtype

