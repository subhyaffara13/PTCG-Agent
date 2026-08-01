
def _map_node_dependencies(graph: onnx.GraphProto, node_to_producers: dict, node_to_consumers: dict):
    graph_inputs = {i.name for i in graph.input}
    initializers = {i.name for i in graph.initializer}

    # map of value name to node that creates it. copy parent values but override if values get shadowed
    producers = {}

    implicit_inputs = set()

    def is_local_value(value):
        return value in producers or value in initializers or value in graph_inputs

    for node in graph.node:
        inputs = list(node.input)

        for attr in node.attribute:
            if attr.HasField("g"):
                subgraph_implicit_inputs = _map_node_dependencies(attr.g, node_to_producers, node_to_consumers)
                inputs += subgraph_implicit_inputs

        for i in inputs:
            if not i:
                # missing optional input
                continue

            if is_local_value(i):
                if i in producers:
                    producer = producers[i]
                    _create_producer_consumer_link(node_to_producers, node_to_consumers, producer, node)
            else:
                implicit_inputs.add(i)

        for o in node.output:
            producers[o] = node

    return implicit_inputs

