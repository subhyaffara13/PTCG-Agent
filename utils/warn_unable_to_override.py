
def warn_unable_to_override(
    node: onnx.NodeProto,
    what_str: str,
    tensor_name: str,
    io_kind: str,
):
    logging.warning(
        f"Unable to override {what_str} for {node.op_type} node's {io_kind} "
        "because it has already been overridden! Check the initial quantization overrides provided "
        "to get_qnn_qdq_config() if the generated QDQ model does not run on QNN EP. "
        f"Node name: {node.name}, {io_kind} name: {tensor_name}"
    )

