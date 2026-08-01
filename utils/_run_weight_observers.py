
def _run_weight_observers(observed: GraphModule, backend_config: BackendConfig) -> None:
    """Extract the subgraph that produces the weight for dynamic quant
    or weight only quant node and run the subgraph to observe the weight.
    Note that the observers of dynamic quant or weight only quant ops are
    run during the convert step.
    """
    for node in observed.graph.nodes:
        if node.op != "call_function":
            continue
        for node_arg in node.args:
            # node_arg is weight
            if node_arg and node_arg_is_weight(node, node_arg):
                weight_observer_nodes = collect_producer_nodes(node_arg)
                if weight_observer_nodes is None:
                    continue
                weight_observer_module = graph_module_from_producer_nodes(
                    observed, weight_observer_nodes
                )
                # run the weight observer
                weight_observer_module()

