
def get_producer_consumer_maps(graph: onnx.GraphProto):
    """
    Get maps for connections between the node that produces each value and the nodes that consume the value.
    Processing includes subgraphs. As the map key is a Node instance from the Graph there should be no ambiguity.
    :param graph: Graph to process.
    :return: Tuple with two maps.
             First is node_to_producers map of a node to set of all nodes producing input it consumes.
             Second is node_to_consumers map of a node to set of all nodes consuming output it creates.
             e.g. NodeA and NodeB provide inputs to NodeC. NodeC provides input to NodeD
             node_to_consumers[NodeA] = set([NodeC])
             node_to_consumers[NodeB] = set([NodeC])
             node_to_producers[NodeC] = set([NodeA, NodeB])
             node_to_consumers[NodeC] = set([NodeD])
             node_to_producers[NodeD] = set([NodeC])
    """

    # use a hash of the object id for NodeProto.
    # we need this for the partitioning checker where we keep maps with nodes as the key.
    onnx.NodeProto.__hash__ = lambda self: id(self)

    node_to_producers = {}  # map of node instance to nodes producing input values it consumes
    node_to_consumers = {}  # map of node instance to nodes consuming output values it produces

    implicit_inputs = _map_node_dependencies(graph, node_to_producers, node_to_consumers)

    # top level graph should have no implicit inputs
    if implicit_inputs:
        raise ValueError(
            f"This appears to be an invalid model with missing inputs of {','.join(sorted(implicit_inputs))}"
        )

    return node_to_producers, node_to_consumers

