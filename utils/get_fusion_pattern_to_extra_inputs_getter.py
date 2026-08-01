
def get_fusion_pattern_to_extra_inputs_getter(
    backend_config: BackendConfig,
) -> dict[Pattern, Callable]:
    """Get a map from fusion pattern to a function that returns extra input nodes
    from the fusion pattern, in the order required by the root node. This is optional,
    if not specified, we will not copy over any extra inputs for the root node.
    Example:
    # Let's say we have the pattern (torch.add, MatchAllNode, (torch.nn.BatchNorm2d, torch.nn.Conv2d))
    # and root node is torch.nn.Conv2d, and the node in MatchAllNode would be an extra
    # argument to the fused module, we can unpack the pattern and return the node at
    # MatchAllNode here
    # we can implement extra_inputs_getter as follows:
    def extra_inputs_getter(pattern) -> List[Any]:
        add, extra_input, conv_pattern = pattern
        return [extra_input]
    """
    extra_inputs_getter_mapping: dict[Pattern, Callable] = {}
    for pattern, config in backend_config._pattern_complex_format_to_config.items():
        if config._extra_inputs_getter is not None:
            extra_inputs_getter_mapping[pattern] = config._extra_inputs_getter
    return extra_inputs_getter_mapping

