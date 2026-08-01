
def _get_input_node_specs(
    node: Node, placement_strategies: dict[Node, OpSpec]
) -> tuple[DTensorSpec, ...]:
    """
    Get the input specs of a node.
    """
    input_specs_list: list[DTensorSpec] = []
    for input_arg in node.all_input_nodes:
        if input_arg in placement_strategies:
            output_spec = placement_strategies[input_arg].output_specs
            if not isinstance(output_spec, DTensorSpec):
                raise AssertionError
            input_specs_list.append(output_spec)
        else:
            raise ValueError(f"{input_arg} does not have output_spec populated.")
    return tuple(input_specs_list)

