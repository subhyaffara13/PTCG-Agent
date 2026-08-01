
def _add_onnxscript_fn(
    model_bytes: bytes,
    custom_opsets: Mapping[str, int],
) -> bytes:
    """Insert model-included custom onnx-script function into ModelProto"""
    try:
        import onnx
    except ImportError as e:
        raise errors.OnnxExporterError("Module onnx is not installed!") from e

    # For > 2GB model, onnx.load_fromstring would fail. However, because
    # in _export_onnx, the tensors should be saved separately if the proto
    # size > 2GB, and if it for some reason did not, the model would fail on
    # serialization anyway in terms of the protobuf limitation. So we don't
    # need to worry about > 2GB model getting here.
    model_proto = onnx.load_model_from_string(model_bytes)  # type: ignore[attr-defined]

    # Iterate graph nodes to insert only the included custom
    # function_proto into model_proto
    onnx_function_list = []  # type: ignore[var-annotated]
    included_node_func: set[str] = set()
    # onnx_function_list and included_node_func are expanded in-place
    _find_onnxscript_op(
        model_proto.graph, included_node_func, custom_opsets, onnx_function_list
    )

    if onnx_function_list:
        model_proto.functions.extend(onnx_function_list)
        model_bytes = model_proto.SerializeToString()
    return model_bytes

