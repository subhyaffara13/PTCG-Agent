
def graph_iterator(model, func):
    graph_queue = [model.graph]
    while graph_queue:
        graph = graph_queue.pop(0)
        func(graph)
        for node in graph.node:
            for attr in node.attribute:
                if attr.type == onnx_pb.AttributeProto.AttributeType.GRAPH:
                    assert isinstance(attr.g, onnx_pb.GraphProto)
                    graph_queue.append(attr.g)
                if attr.type == onnx_pb.AttributeProto.AttributeType.GRAPHS:
                    for g in attr.graphs:
                        assert isinstance(g, onnx_pb.GraphProto)
                        graph_queue.append(g)

