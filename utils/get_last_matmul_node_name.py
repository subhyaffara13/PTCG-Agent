
def get_last_matmul_node_name(raw_onnx_model: str):
    model = onnx.load(raw_onnx_model)
    onnx_model = OnnxModel(model)
    output_name_to_node = onnx_model.output_name_to_node()

    assert model.graph.output[0].name in output_name_to_node
    node = output_name_to_node[model.graph.output[0].name]
    if node.op_type == "MatMul":
        logger.info(f"Found last MatMul node for logits: {node.name}")
        return node.name

    logger.warning(f"Failed to find MatMul node for logits. Found {node.op_type} of node {node.name}")
    return None

