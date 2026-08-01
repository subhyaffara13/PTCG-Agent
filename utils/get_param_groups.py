
def get_param_groups(
    inputs: list[Node], params: list[Node], reverse_edges_dict
) -> list[dict[str, Any]]:
    """
    Given a list of inputs and a list of parameters, return a list of parameter
    groups, where each group contains the parameters and the intermediates that
    are connected to the parameters.

    The returned list of parameter groups is a list of dictionaries, where each
    dictionary contains the following keys:
    - "params": a set of parameters
    - "intermediates": a set of intermediates

    The returned list of parameter groups is a list of dictionaries,
    """
    # reverse graph that starts with inputs, and goes up to the dOutput or the loss,
    # but omits weights and any subgraphs connecting weights to this closure
    inputs_closure, _ = reverse_closure(inputs, set(), reverse_edges_dict)
    param_groups: dict[Node, dict[str, set]] = dict()  # keyed on intermediates
    for param in params:
        closure, intersected = reverse_closure(
            [param], inputs_closure, reverse_edges_dict
        )
        param_group: dict[str, set] = {
            "params": {param},
            "intermediates": intersected,
        }
        for input_node in intersected:
            existing = param_groups.get(input_node)
            if existing is not None:
                existing["params"] = existing["params"].union(param_group["params"])
                existing["intermediates"] = existing["intermediates"].union(
                    param_group["intermediates"]
                )
                param_group = existing
            else:
                param_groups[input_node] = param_group

    # Sanity check: union of all param_groups params should be equal to all params
    union_params: set[Node] = set()
    seen_ids: set[int] = set()
    unique_param_groups = []
    for param_group in param_groups.values():
        if id(param_group) not in seen_ids:
            seen_ids.add(id(param_group))
            unique_param_groups.append(param_group)
            union_params = union_params.union(param_group["params"])

    # The assert will only be true if the input tensor requires gradients,
    # otherwise the autograd graph will miss the first layer of inputs
    # assert union_params == set(params)
    return unique_param_groups

