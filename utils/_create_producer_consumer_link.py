
def _create_producer_consumer_link(
    node_to_producers: dict, node_to_consumers: dict, producer: onnx.NodeProto, consumer: onnx.NodeProto
):
    """
    Create links between two nodes for a value produced by one and consumed by the other.
    :param node_to_producers: Map of NodeProto to set of nodes that produce values the node consumes as inputs.
    :param node_to_consumers: Map of NodeProto to set of nodes that consume values the node produces as outputs.
    :param producer: Producer node
    :param consumer: Consumer node
    """

    if consumer not in node_to_producers:
        node_to_producers[consumer] = set()

    if producer not in node_to_consumers:
        node_to_consumers[producer] = set()

    # add entry mapping this node to the producer of this input
    node_to_producers[consumer].add(producer)
    node_to_consumers[producer].add(consumer)

